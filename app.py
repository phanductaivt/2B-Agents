from __future__ import annotations

import argparse
import importlib.util
import logging
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECTS_DIR = BASE_DIR / "projects"
WORKSPACE_DIR = BASE_DIR / "workspace"
DEFAULT_PROJECT_NAME = "ticket-booking-improvement"
ARTIFACT_CATALOG_PATH = BASE_DIR / "system" / "artifacts" / "artifact-catalog.yaml"
GATES_CONFIG_PATH = BASE_DIR / "system" / "configs" / "gates.yaml"
CHECKLIST_TEMPLATES_DIR = BASE_DIR / "system" / "templates" / "checklists"


def load_local_module(module_name: str, relative_path: str):
    """Load a small helper file from this workspace."""
    module_path = BASE_DIR / relative_path
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


reader = load_local_module("files_reader", "system/tools/files/reader.py")
writer = load_local_module("files_writer", "system/tools/files/writer.py")
status_manager = load_local_module("status_manager", "system/tools/project/status_manager.py")
console_logger = load_local_module("console_logger", "system/tools/logging/console_logger.py")
project_paths = load_local_module("project_paths", "system/tools/project/project_paths.py")


def parse_arguments() -> argparse.Namespace:
    """Parse simple CLI arguments for automated runs."""
    parser = argparse.ArgumentParser(description="Run the BA-led project pipeline.")
    parser.add_argument("--project", help="Run only one project by name.")
    parser.add_argument("--requirement", help="Run only one requirement file name in a project.")
    parser.add_argument("--input", help="(Legacy alias) requirement file name in a project.")
    parser.add_argument("--force", action="store_true", help="Re-run even if outputs exist.")
    parser.add_argument("--dashboard", action="store_true", help="Only refresh the dashboard.")
    parser.add_argument(
        "--sync-context",
        action="store_true",
        help="Run safe Level 1 context sync and exit.",
    )
    parser.add_argument(
        "--mode",
        choices=["full", "controlled"],
        default="full",
        help="full = one-shot package generation, controlled = artifact/stage execution.",
    )
    parser.add_argument(
        "--artifact",
        help="Artifact name for controlled mode (example: frs, wireframe, ui).",
    )
    parser.add_argument(
        "--stage",
        help="Stage name for controlled mode (example: clarification, ba-core, design, fe-prototype, review).",
    )
    parser.add_argument(
        "--override-gate",
        action="store_true",
        help="Allow artifact run even when upstream gate is blocked. Use carefully.",
    )
    return parser.parse_args()


def configure_logging() -> None:
    """Write run logs to workspace/logs/run.log."""
    logs_dir = BASE_DIR / "workspace" / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_path = logs_dir / "run.log"
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def log_info(message: str) -> None:
    console_logger.info(message)
    logging.info(message)


def log_success(message: str) -> None:
    console_logger.success(message)
    logging.info(message)


def log_warning(message: str) -> None:
    console_logger.warning(message)
    logging.warning(message)


def log_error(message: str) -> None:
    console_logger.error(message)
    logging.error(message)


def log_step(scope: str, message: str) -> None:
    console_logger.step(scope, message)
    logging.info(f"[{scope.upper()}] {message}")


def log_skipped(message: str) -> None:
    if hasattr(console_logger, "skipped"):
        console_logger.skipped(message)
    else:
        console_logger.warning(f"SKIPPED: {message}")
    logging.info(f"[SKIPPED] {message}")


def log_blocked(message: str) -> None:
    if hasattr(console_logger, "blocked"):
        console_logger.blocked(message)
    else:
        console_logger.warning(f"BLOCKED: {message}")
    logging.warning(f"[BLOCKED] {message}")


def log_context_load(
    project_name: str,
    global_loaded: list[str],
    global_missing: list[str],
    project_loaded: list[str],
    project_missing: list[str],
) -> None:
    """Write one context loading record into workspace/logs/context-load.log."""
    logs_dir = BASE_DIR / "workspace" / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_path = logs_dir / "context-load.log"
    lines = [
        f"Project: {project_name}",
        f"Global loaded: {', '.join(global_loaded) if global_loaded else 'None'}",
        f"Global missing: {', '.join(global_missing) if global_missing else 'None'}",
        f"Project loaded: {', '.join(project_loaded) if project_loaded else 'None'}",
        f"Project missing: {', '.join(project_missing) if project_missing else 'None'}",
        "---",
    ]
    with log_path.open("a", encoding="utf-8") as file:
        file.write("\n".join(lines) + "\n")


def read_playbook_name(playbook_file: Path) -> str:
    """Read the playbook name from YAML with a simple text scan."""
    playbook_text = reader.read_text_file(playbook_file)
    for line in playbook_text.splitlines():
        if line.startswith("name:"):
            return line.split(":", 1)[1].strip()
    return playbook_file.parent.name


def collect_clean_lines(raw_text: str) -> list[str]:
    """Turn raw input text into a short list of useful business lines."""
    cleaned_lines: list[str] = []
    for raw_line in raw_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        line = line.lstrip("- ").strip()
        line = line.lstrip("#").strip()
        if line:
            cleaned_lines.append(line)
    return cleaned_lines


def extract_markdown_list_items(text: str) -> list[str]:
    """Read simple bullet points from a Markdown note."""
    items: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("- "):
            items.append(line[2:].strip())
    return items


def first_meaningful_line(text: str) -> str:
    """Return the first readable line from a note or README."""
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line and not line.startswith("#") and not line.startswith("- "):
            return line
    return ""


def unique_items(items: list[str]) -> list[str]:
    """Keep only the first appearance of each line."""
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        key = item.lower()
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


def extract_keywords(text: str) -> list[str]:
    """Pull simple keywords from a sentence for loose alignment checks."""
    words = [
        word.strip(".,:;()[]{}")
        for word in text.lower().split()
        if len(word.strip(".,:;()[]{}")) >= 4
    ]
    return words


def flow_alignment_issues(bpmn_text: str, flow_steps: list[str], flow_name: str) -> list[str]:
    """Check that BPMN contains at least one keyword from each flow step."""
    issues: list[str] = []
    bpmn_lower = bpmn_text.lower()
    missing_steps: list[str] = []

    for step in flow_steps:
        keywords = extract_keywords(step)
        if not keywords:
            continue
        if not any(keyword in bpmn_lower for keyword in keywords):
            missing_steps.append(step)

    if missing_steps:
        issues.append(
            f"BPMN diagram does not reflect these {flow_name} steps: "
            + "; ".join(missing_steps)
            + "."
        )
    return issues


def choose_user_role(raw_text: str) -> str:
    lower_text = raw_text.lower()
    if "member" in lower_text:
        return "member"
    if "customer" in lower_text:
        return "customer"
    if "support" in lower_text:
        return "support agent"
    if "manager" in lower_text:
        return "manager"
    return "user"


def has_functional_scope(
    acceptance_criteria: list[str],
    functional_requirements: list[str],
) -> bool:
    """Treat the request as functional when it already contains behavior the team can build."""
    return bool(acceptance_criteria or functional_requirements)


def detect_scenario(project_domain: str, raw_text: str) -> str:
    """Pick a simple business scenario so the sample outputs feel realistic."""
    lower_text = raw_text.lower()
    lower_domain = project_domain.lower()

    if (
        "loyalty" in lower_text
        or "points" in lower_text
        or "tier" in lower_text
        or lower_domain == "loyalty"
    ):
        return "loyalty"
    if (
        "ticket" in lower_text
        or "booking" in lower_text
        or "refund" in lower_text
        or "fare" in lower_text
        or lower_domain == "ticketing"
    ):
        return "ticketing"
    if "order" in lower_text:
        return "order-status"
    return "generic-status"


def build_default_business_rules(scenario: str) -> list[str]:
    if scenario == "ticketing":
        return [
            "Only eligible tickets can be changed online.",
            "The customer must see change fees before confirming the update.",
            "Refund or reissue steps must follow approved fare rules and channel policy.",
            "Change eligibility must be checked against the latest fare and ticket rules.",
            "If a booking is not eligible, the system must show the reason and the next support path.",
        ]
    if scenario == "loyalty":
        return [
            "Only posted transactions can add to available loyalty points.",
            "Expired points must be shown separately from available points.",
            "Tier progress must follow approved membership rules.",
            "Pending activity must not change available points until posting.",
            "If tier data is missing, the system must show guidance instead of a blank panel.",
        ]
    if scenario == "order-status":
        return [
            "Only approved order statuses such as confirmed, packed, and shipped should be shown.",
            "Customers should only see statuses for their own orders.",
            "If an order status is missing or out of release scope, the page should guide the customer to support.",
            "Status data must be refreshed from the approved source before display.",
            "If the status service is unavailable, the page must show a fallback message.",
        ]
    return [
        "Only approved business status values should be shown to the end user.",
        "The user should only see information for the correct record or item.",
        "If no valid business value is available, the system should guide the user to the next support path.",
    ]


def build_feature_list(scenario: str) -> list[dict[str, object]]:
    """Create a simple Level 1 / Level 2 / Level 3 feature structure."""
    if scenario == "ticketing":
        return [
            {
                "level_1": "Booking Management",
                "level_2": [
                    {
                        "name": "Change Eligibility",
                        "level_3": [
                            "Check Whether Ticket Can Be Changed Online",
                            "Show Why A Booking Is Not Eligible",
                        ],
                    },
                    {
                        "name": "Ticket Modification",
                        "level_3": [
                            "Show Available Change Options",
                            "Show Change Fee Before Confirmation",
                        ],
                    },
                ],
            },
            {
                "level_1": "Support Guidance",
                "level_2": [
                    {
                        "name": "Fallback Handling",
                        "level_3": [
                            "Show Support Path When Change Is Not Allowed",
                            "Explain Refund Or Reissue Next Step",
                        ],
                    }
                ],
            },
        ]
    if scenario == "loyalty":
        return [
            {
                "level_1": "Loyalty Overview",
                "level_2": [
                    {
                        "name": "Points Visibility",
                        "level_3": [
                            "Show Available Points",
                            "Show Expired Points Separately",
                        ],
                    },
                    {
                        "name": "Tier Progress",
                        "level_3": [
                            "Show Current Tier",
                            "Show Progress Toward Next Tier",
                        ],
                    },
                ],
            },
            {
                "level_1": "Activity History",
                "level_2": [
                    {
                        "name": "Member Activity",
                        "level_3": [
                            "Show Recent Loyalty Transactions",
                            "Explain Missing Or Delayed Loyalty Activity",
                        ],
                    }
                ],
            },
        ]
    if scenario == "order-status":
        return [
            {
                "level_1": "Order Management",
                "level_2": [
                    {
                        "name": "Status Visibility",
                        "level_3": [
                            "Show Latest Approved Status",
                            "Show Status Timeline For Current Order",
                        ],
                    },
                    {
                        "name": "Order Access Control",
                        "level_3": [
                            "Show Status For The Correct Customer Order",
                            "Block Unauthorized Order View",
                        ],
                    },
                ],
            },
            {
                "level_1": "Support Guidance",
                "level_2": [
                    {
                        "name": "Fallback Handling",
                        "level_3": [
                            "Show Missing Status Message",
                            "Show Service Unavailable Message",
                        ],
                    },
                    {
                        "name": "Help Paths",
                        "level_3": [
                            "Explain Next Step To Customer",
                            "Offer Contact Support Path",
                        ],
                    },
                ],
            },
        ]
    return [
        {
            "level_1": "Status Management",
            "level_2": [
                {
                    "name": "Status Visibility",
                    "level_3": [
                        "Show Latest Approved Status",
                        "Show Status Detail For The Current Record",
                    ],
                },
                {
                    "name": "Access Control",
                    "level_3": [
                        "Show Data For The Correct User",
                        "Block Unauthorized Record View",
                    ],
                },
            ],
        },
        {
            "level_1": "Guidance And Exceptions",
            "level_2": [
                {
                    "name": "Fallback Messages",
                    "level_3": [
                        "Show Missing Status Guidance",
                        "Show Temporary Service Issue Message",
                    ],
                },
                {
                    "name": "Support Options",
                    "level_3": [
                        "Explain The Next Step",
                        "Offer A Help Path",
                    ],
                },
            ],
        },
    ]


def build_scenario_defaults(scenario: str, user_role: str) -> dict[str, object]:
    """Return simple business defaults for each demo scenario."""
    if scenario == "ticketing":
        return {
            "story_text": (
                f"As a {user_role}, I want to change my booking in a guided self-service flow "
                "so that I do not need to contact support for common ticket changes."
            ),
            "business_problem": "Customers call support because ticket change rules and next steps are not clear online.",
            "functional_summary": "The portal must guide the customer through booking change eligibility, fees, and next steps.",
            "bpmn_steps": [
                "flowchart TD",
                "    A[Start] --> B[Customer opens booking change page]",
                "    B --> C[System checks booking eligibility]",
                "    C --> D{Online change allowed?}",
                "    D -->|Yes| E[Show change options and fees]",
                "    D -->|No| F[Show support or refund guidance]",
                "    E --> G[Customer confirms change]",
                "    G --> H[System updates booking]",
                "    F --> I[End]",
                "    H --> I[End]",
            ],
            "acceptance_criteria": [
                "Given a customer opens the booking change page, when eligibility is checked, then the system shows whether the booking can be changed online.",
                "Given a booking is eligible, when change options are shown, then the change fee is displayed before confirmation.",
                "Given a booking is not eligible, when the customer opens the change page, then support or refund guidance is displayed.",
                "Given the booking does not belong to the customer, when they attempt to view change options, then access is blocked.",
            ],
            "main_flow": [
                "Customer opens the booking change page.",
                "System checks eligibility for the selected booking.",
                "System shows change options and fees.",
                "Customer confirms the change.",
                "System updates the booking and shows the confirmation.",
            ],
            "alternative_flows": [
                "If the booking is not eligible, show the reason and the support or refund path.",
                "If fare rules cannot be loaded, show a fallback message and stop the change flow.",
                "If the fee is zero, still show a clear confirmation step before updating.",
            ],
            "functional_requirements": [
                "FR-1: The customer can open the booking change page and review eligibility for the selected booking.",
                "FR-2: The system displays allowed change options and the related fee before confirmation.",
                "FR-3: The page displays support or refund guidance when the booking is not eligible for online change.",
                "FR-4: The page prevents the customer from seeing or changing another customer's booking.",
            ],
            "validations": [
                "Show only valid change options for the selected booking.",
                "Show fee information before final confirmation.",
                "Do not show another customer's booking details.",
            ],
            "edge_cases": [
                "If the booking is not eligible for online change, display the reason and the next support path.",
                "If fare rules cannot be loaded, show a fallback message instead of invalid fee data.",
                "If the change fee is zero, still show a clear confirmation step.",
                "If the selected booking does not belong to the customer, do not display modification options.",
            ],
            "dependencies": [
                "Booking rules service is available.",
                "Fare rules and refund rules are approved by business stakeholders.",
            ],
            "business_goals": [
                "Reduce avoidable booking-change support calls.",
                "Help customers understand ticket change rules earlier.",
                "Create a small first release for self-service booking change.",
            ],
            "scope": [
                "Show booking change eligibility and the first supported self-service change path.",
                "Display change fees before confirmation.",
                "Guide the customer to support or refund help when online change is not allowed.",
            ],
        }
    if scenario == "loyalty":
        return {
            "story_text": (
                f"As a {user_role}, I want to view my points and tier progress clearly "
                "so that I understand my loyalty status without contacting support."
            ),
            "business_problem": "Members contact support because loyalty points, tier progress, and recent activity are not clear enough.",
            "functional_summary": "The portal must show available points, tier progress, and recent loyalty activity for the current member.",
            "bpmn_steps": [
                "flowchart TD",
                "    A[Start] --> B[Member opens loyalty page]",
                "    B --> C[System loads points and tier data]",
                "    C --> D{Valid loyalty data available?}",
                "    D -->|Yes| E[Show points, tier progress, and activity]",
                "    D -->|No| F[Show guidance for missing or delayed data]",
                "    E --> G[End]",
                "    F --> G[End]",
            ],
            "acceptance_criteria": [
                "Given a member opens the loyalty overview, when data is available, then the page shows available points for the current account.",
                "Given loyalty data is available, when the page loads, then current tier and progress toward the next tier are displayed.",
                "Given activity data is available, when the member views the page, then recent loyalty activity is displayed.",
                "Given loyalty data is missing or delayed, when the page loads, then a guidance message is displayed.",
            ],
            "main_flow": [
                "Member opens the loyalty overview page.",
                "System loads points, tier progress, and recent activity.",
                "System displays the loyalty summary to the member.",
            ],
            "alternative_flows": [
                "If loyalty data is delayed, show a guidance message and hide incomplete totals.",
                "If activity data is missing, show a placeholder and a support path.",
                "If the member account is invalid, show an access error message.",
            ],
            "functional_requirements": [
                "FR-1: The member can open the loyalty overview page and view available points for the current account.",
                "FR-2: The system displays the current tier and progress toward the next tier using approved membership rules.",
                "FR-3: The page displays recent loyalty activity for the current member account.",
                "FR-4: The page displays guidance when loyalty data is unavailable or delayed.",
            ],
            "validations": [
                "Show only the current member's loyalty data.",
                "Separate available points from expired points.",
                "Keep tier wording aligned with approved business labels.",
            ],
            "edge_cases": [
                "If loyalty data is delayed, display a clear message instead of blank sections.",
                "If a transaction is pending, do not add it to available points before posting.",
                "If points have expired, show them separately from available points.",
                "If the member account is not valid, do not display another member's loyalty data.",
            ],
            "dependencies": [
                "Loyalty data service is available.",
                "Tier rules and point labels are approved by business stakeholders.",
            ],
            "business_goals": [
                "Reduce avoidable loyalty-related support calls.",
                "Improve member confidence in points and tier progress.",
                "Create a simple first dashboard release for web users.",
            ],
            "scope": [
                "Show available points, tier progress, and recent activity in one member view.",
                "Separate available values from expired or unavailable values clearly.",
                "Guide the member when loyalty data is delayed or missing.",
            ],
        }
    if scenario == "order-status":
        return {
            "story_text": (
                f"As a {user_role}, I want to view clear order status updates "
                "so that I understand order progress without contacting support."
            ),
            "business_problem": "Customers contact support because they cannot see order progress clearly.",
            "functional_summary": "The portal must display the latest approved order status to the customer.",
            "bpmn_steps": [
                "flowchart TD",
                "    A[Start] --> B[Customer opens order page]",
                "    B --> C[System loads latest approved order status]",
                "    C --> D{Valid status available?}",
                "    D -->|Yes| E[Show approved order status]",
                "    D -->|No| F[Show support guidance]",
                "    E --> G[End]",
                "    F --> G[End]",
            ],
            "acceptance_criteria": [
                "Given a customer opens their order page, when a valid status exists, then the approved status label is displayed.",
                "Given the status label is displayed, when the status is shown, then it matches approved business wording.",
                "Given a valid status exists, when the page loads, then the latest approved status value is displayed.",
                "Given no valid status exists, when the page loads, then a support guidance message is displayed.",
            ],
            "main_flow": [
                "Customer opens the order page.",
                "System loads the latest approved status.",
                "System displays the status to the customer.",
            ],
            "alternative_flows": [
                "If no valid status is available, show a support guidance message.",
                "If the status service is unavailable, show a fallback message and stop the status display.",
                "If the order is outside scope, show the next support path.",
            ],
            "functional_requirements": [
                "FR-1: The user can open the page and view the latest approved status for the current order.",
                "FR-2: The system displays only approved status values that are in scope for the release.",
                "FR-3: The page displays a support guidance message if no valid status is available.",
                "FR-4: The page prevents the user from seeing another user's order details.",
            ],
            "validations": [
                "Show only valid and approved order status values.",
                "Do not show another customer's order.",
                "Keep wording aligned with approved status labels.",
            ],
            "edge_cases": [
                "If no status is returned, display a support guidance message instead of leaving the page blank.",
                "If the status service is temporarily unavailable, display a fallback message and avoid showing incorrect data.",
                "If the order is cancelled but cancelled is outside first-release scope, guide the user to support.",
                "If the user tries to open an order that does not belong to them, do not display order details.",
            ],
            "dependencies": [
                "Order status data source is available.",
                "Business status labels are approved by business stakeholders.",
            ],
            "business_goals": [
                "Reduce avoidable support effort.",
                "Improve user confidence through clearer order status visibility.",
                "Create a simple first release that is easy to review and improve.",
            ],
            "scope": [
                "Show the latest approved order status in the user-facing page.",
                "Support the first release with a simple visible flow.",
                "Keep the first release focused on one clear feature slice.",
            ],
        }
    return {
        "story_text": (
            f"As a {user_role}, I want to view clear status updates "
            "so that I understand progress without extra follow-up."
        ),
        "business_problem": "Users do not have clear visibility into the current status.",
        "functional_summary": "The page must display the latest approved status to the user.",
        "bpmn_steps": [
            "flowchart TD",
            "    A[Start] --> B[User opens status page]",
            "    B --> C[System loads latest approved status]",
            "    C --> D{Valid status available?}",
            "    D -->|Yes| E[Show status details]",
            "    D -->|No| F[Show fallback guidance]",
            "    E --> G[End]",
            "    F --> G[End]",
        ],
        "acceptance_criteria": [
            "Given the user opens the status page, when a valid status exists, then the approved status label is displayed.",
            "Given a status is displayed, when the label appears, then it matches approved business wording.",
            "Given a valid status exists, when the page loads, then the latest approved status value is displayed.",
            "Given no valid status exists, when the page loads, then a guidance message is displayed.",
        ],
        "main_flow": [
            "User opens the status page.",
            "System loads the latest approved status.",
            "System displays the status to the user.",
        ],
        "alternative_flows": [
            "If no valid status is available, show a guidance message.",
            "If the status service is unavailable, show a fallback message.",
        ],
        "functional_requirements": [
            "FR-1: The user can open the page and view the latest approved status for the current record.",
            "FR-2: The system displays only business-approved values that are in scope for the release.",
            "FR-3: The page displays guidance if no valid status is available.",
            "FR-4: The page prevents the user from seeing another user's record details.",
        ],
        "validations": [
            "Show only valid and approved values.",
            "Do not show another user's record.",
            "Keep wording aligned with business-approved labels.",
        ],
        "edge_cases": [
            "If no data is returned, display a guidance message instead of leaving the page blank.",
            "If the service is temporarily unavailable, display a fallback message and avoid showing incorrect data.",
            "If a value is outside first-release scope, guide the user to support.",
            "If the user tries to open a record that does not belong to them, do not display details.",
        ],
        "dependencies": [
            "Status data source is available.",
            "Business labels are approved by business stakeholders.",
        ],
        "business_goals": [
            "Reduce avoidable support effort.",
            "Improve user confidence through clearer visibility.",
            "Create a simple first release that is easy to review and improve.",
        ],
        "scope": [
            "Show the latest approved status in the user-facing page.",
            "Support the first release with a simple visible flow.",
            "Keep the first release focused on one clear feature slice.",
        ],
    }


def load_knowledge_bundle(
    project_dir: Path,
    auto_context: dict[str, object] | None = None,
) -> dict[str, object]:
    """Load project knowledge and include auto-loaded context package."""
    project_knowledge = reader.read_project_knowledge(project_dir)
    shared_knowledge = {
        "glossary": reader.read_text_if_exists(BASE_DIR / "system" / "knowledge/glossary/glossary-template.md"),
        "company": reader.read_text_if_exists(BASE_DIR / "system" / "knowledge/company/README.md"),
        "domain": reader.read_text_if_exists(BASE_DIR / "system" / "knowledge/domain/README.md"),
        "notes": reader.read_text_if_exists(BASE_DIR / "system" / "knowledge/projects/README.md"),
    }

    project_file_names = {
        "glossary": "glossary.md",
        "business_rules": "business-rules.md",
        "notes": "notes.md",
    }
    project_files_loaded = [
        project_file_names[name] for name, text in project_knowledge.items() if text.strip()
    ]
    shared_files_loaded = [
        path
        for path, text in {
            "system/knowledge/glossary/glossary-template.md": shared_knowledge["glossary"],
            "system/knowledge/company/README.md": shared_knowledge["company"],
            "system/knowledge/domain/README.md": shared_knowledge["domain"],
            "system/knowledge/projects/README.md": shared_knowledge["notes"],
        }.items()
        if str(text).strip()
    ]

    return {
        "project": project_knowledge,
        "shared": shared_knowledge,
        "project_files_loaded": project_files_loaded,
        "shared_files_loaded": shared_files_loaded,
        "auto_context": auto_context or {
            "text": "",
            "global_loaded_files": [],
            "global_missing_files": [],
            "project_loaded_files": [],
            "project_missing_files": [],
        },
        "priority": "global context -> project context -> project knowledge -> shared knowledge -> generic fallback",
    }


def build_ba_package(
    raw_text: str,
    project_config: dict[str, object],
    knowledge_bundle: dict[str, object],
    scenario_context: dict[str, object],
) -> dict[str, object]:
    """Create the BA Agent output bundle."""
    def as_list(value: object) -> list[str]:
        if isinstance(value, list):
            return [str(item) for item in value if str(item).strip()]
        return []

    lines = collect_clean_lines(raw_text)
    lower_text = raw_text.lower()
    title = lines[0] if lines else "Requirement clarification request"
    user_role = choose_user_role(raw_text)
    scenario = str(scenario_context.get("scenario_name", "generic"))
    defaults_raw = scenario_context.get("scenario_data", {})
    defaults = defaults_raw if isinstance(defaults_raw, dict) else {}

    project_business_rules = extract_markdown_list_items(
        str(knowledge_bundle["project"]["business_rules"])
    )
    auto_context_text = str(knowledge_bundle["auto_context"].get("text", ""))
    context_hint = first_meaningful_line(auto_context_text)
    knowledge_note = first_meaningful_line(str(knowledge_bundle["project"]["notes"]))
    project_description = str(project_config.get("description", "")).strip()

    summary = f"{title}: {' '.join(lines[1:3])}" if len(lines) > 1 else title
    known_facts = lines[1:5] or ["The input is short and needs more detail."]
    if project_description:
        known_facts.append(f"Project description: {project_description}")
    if knowledge_note:
        known_facts.append(f"Project note: {knowledge_note}")
    if context_hint:
        known_facts.append(f"Auto context hint: {context_hint}")
    known_facts = unique_items(known_facts)[:6]

    assumptions: list[str] = []
    if "metric" not in lower_text and "success" not in lower_text:
        assumptions.append("A measurable success metric is still missing.")
    if not project_business_rules and "rule" not in lower_text and "policy" not in lower_text:
        assumptions.append("Detailed business rules still need confirmation.")
    if "integration" not in lower_text and "api" not in lower_text and "system" not in lower_text:
        assumptions.append("System integration details are not described yet.")

    open_questions: list[str] = []
    if user_role == "user" and "user" not in lower_text:
        open_questions.append("Who is the main user or stakeholder for this requirement?")
    if "release" not in lower_text and "date" not in lower_text:
        open_questions.append("Is there a target release or milestone for this work?")
    open_questions.append("Are there any approvals, exceptions, or out-of-scope cases to capture?")

    default_rules = as_list(defaults.get("default_business_rules"))
    if project_business_rules:
        business_rules = unique_items(project_business_rules + default_rules)
        rule_source = "project knowledge + system defaults"
    else:
        business_rules = default_rules
        rule_source = "generic fallback"

    frs = {
        "title": title,
        "functional_summary": str(defaults.get("functional_summary", "")),
        "actors": [user_role, "business service"],
        "functional_requirements": as_list(defaults.get("functional_requirements")),
        "main_flow": as_list(defaults.get("main_flow")),
        "alternative_flows": as_list(defaults.get("alternative_flows")),
        "business_rules": business_rules,
        "validations": as_list(defaults.get("validations")),
        "edge_cases": as_list(defaults.get("edge_cases")),
        "dependencies": as_list(defaults.get("dependencies")),
        "open_questions": open_questions,
    }

    acceptance_criteria = as_list(defaults.get("acceptance_criteria"))
    functional_scope_exists = has_functional_scope(
        acceptance_criteria,
        frs["functional_requirements"],
    )
    feature_list_raw = defaults.get("feature_list", [])
    feature_list = (
        feature_list_raw
        if functional_scope_exists and isinstance(feature_list_raw, list)
        else []
    )
    bpmn_steps = as_list(defaults.get("bpmn_steps"))
    story_template = str(defaults.get("story_text", "As a {user_role}, I want a clear flow so that work is easier to complete."))
    story_text = story_template.replace("{user_role}", user_role)

    return {
        "project_name": str(project_config.get("project_name", "")),
        "project_description": project_description,
        "project_owner": str(project_config.get("owner", "")),
        "project_domain": str(project_config.get("domain", "")),
        "project_notes": str(project_config.get("notes", "")),
        "knowledge_priority": str(knowledge_bundle["priority"]),
        "project_files_loaded": list(knowledge_bundle["project_files_loaded"]),
        "shared_files_loaded": list(knowledge_bundle["shared_files_loaded"]),
        "global_context_files_loaded": list(knowledge_bundle["auto_context"].get("global_loaded_files", [])),
        "project_context_files_loaded": list(knowledge_bundle["auto_context"].get("project_loaded_files", [])),
        "business_rule_source": rule_source,
        "scenario_source": str(scenario_context.get("source", "unknown")),
        "scenario_defaults": defaults,
        "scenario": scenario,
        "title": title,
        "summary": summary,
        "known_facts": known_facts,
        "assumptions": assumptions,
        "open_questions": open_questions,
        "next_actions": [
            "Review the BA package with business stakeholders.",
            "Confirm the business rules before UXUI and FE handoff.",
            "Use the approved first slice for downstream implementation.",
        ],
        "business_rules": business_rules,
        "bpmn_mermaid": "\n".join(bpmn_steps),
        "user_story": {
            "title": title,
            "story": story_text,
            "context": "This story comes from the BA clarification, process review, and feature structuring step.",
            "dependencies": "Confirm business rules, release scope, and source system behavior.",
            "invest": [
                "Independent: The story can be delivered without a separate dependency story.",
                "Negotiable: Details such as labels or thresholds can be refined with stakeholders.",
                "Valuable: The outcome reduces effort or improves user confidence.",
                "Estimable: Scope is small enough for a team to size.",
                "Small: The story focuses on one main outcome.",
                "Testable: Acceptance criteria describe observable results.",
            ],
        },
        "acceptance_criteria": acceptance_criteria,
        "brd": {
            "title": title,
            "business_problem": str(defaults.get("business_problem", "")),
            "business_goals": as_list(defaults.get("business_goals")),
            "stakeholders": [
                "Business Analyst",
                "Business Stakeholder",
                "Support Team",
                "End User",
            ],
            "scope": as_list(defaults.get("scope")),
            "business_rules": business_rules,
            "assumptions": assumptions,
            "expected_benefits": [
                "Fewer avoidable support questions.",
                "Better alignment between business and delivery teams.",
            ],
        },
        "frs": frs,
        "functional_scope_exists": functional_scope_exists,
        "feature_list": feature_list,
    }


def build_uxui_package(ba_package: dict[str, object]) -> dict[str, object]:
    """Create the UXUI wireframe package from the BA FRS."""
    title = str(ba_package["title"])
    scenario_defaults = ba_package.get("scenario_defaults", {})
    ux_defaults = scenario_defaults.get("uxui_defaults", {}) if isinstance(scenario_defaults, dict) else {}
    if not isinstance(ux_defaults, dict):
        ux_defaults = {}

    def as_list(value: object) -> list[str]:
        if isinstance(value, list):
            return [str(item) for item in value if str(item).strip()]
        return []

    sketch_lines = as_list(ux_defaults.get("wireframe_sketch"))
    return {
        "title": title,
        "primary_input": "FRS from the BA Agent",
        "screen_goal": str(
            ux_defaults.get(
                "screen_goal",
                "Help the user understand key status and next actions clearly.",
            )
        ),
        "main_sections": as_list(ux_defaults.get("main_sections")),
        "components": as_list(ux_defaults.get("components")),
        "interaction_notes": as_list(ux_defaults.get("interaction_notes")),
        "wireframe_sketch": "\n".join(sketch_lines),
    }


def build_fe_package(
    ba_package: dict[str, object],
    uxui_package: dict[str, object],
    id_map: dict[str, str] | None = None,
) -> dict[str, str]:
    """Create one simple HTML page from the BA FRS and UXUI wireframe."""
    _ = uxui_package
    title = str(ba_package["title"])
    scenario_defaults = ba_package.get("scenario_defaults", {})
    fe_defaults = scenario_defaults.get("fe_defaults", {}) if isinstance(scenario_defaults, dict) else {}
    if not isinstance(fe_defaults, dict):
        fe_defaults = {}

    page_intro = str(fe_defaults.get("intro", "Simple FE demo generated from BA + UXUI defaults."))
    cards_items = fe_defaults.get("cards", [])
    cards_parts: list[str] = []
    if isinstance(cards_items, list):
        for card in cards_items:
            if not isinstance(card, dict):
                continue
            title_value = str(card.get("title", "Section"))
            status_value = str(card.get("status", "")).strip()
            lines_value = card.get("lines", [])
            list_value = card.get("list", [])

            card_lines = [f'      <article class="card">', f"        <h2>{title_value}</h2>"]
            if status_value:
                card_lines.append(f'        <p class="status">{status_value}</p>')
            if isinstance(lines_value, list):
                for line in lines_value:
                    card_lines.append(f"        <p>{str(line)}</p>")
            if isinstance(list_value, list) and list_value:
                card_lines.append("        <ul>")
                for item in list_value:
                    card_lines.append(f"          <li>{str(item)}</li>")
                card_lines.append("        </ul>")
            card_lines.append("      </article>")
            cards_parts.append("\n".join(card_lines))
    if not cards_parts:
        cards_parts.append(
            "\n".join(
                [
                    '      <article class="card">',
                    "        <h2>Overview</h2>",
                    "        <p>No scenario-specific FE card defaults were provided.</p>",
                    "      </article>",
                ]
            )
        )
    cards = "\n\n".join(cards_parts)

    id_comment = ""
    if id_map:
        id_comment = (
            f"  <!-- UI ID: {id_map.get('ui', 'UI-000')} | "
            f"FEAT ID: {id_map.get('feat', 'FEAT-000')} | "
            f"FR ID: {id_map.get('fr', 'FR-000')} | "
            f"REQ ID: {id_map.get('req', 'REQ-000')} -->\n"
        )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <style>
    body {{
      margin: 0;
      font-family: Arial, sans-serif;
      background: #f5f4ef;
      color: #1f1f1f;
    }}
    .page {{
      max-width: 960px;
      margin: 40px auto;
      padding: 24px;
    }}
    .hero {{
      background: #ffffff;
      border: 1px solid #d8d2c8;
      border-radius: 16px;
      padding: 24px;
      margin-bottom: 20px;
    }}
    .grid {{
      display: grid;
      gap: 20px;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    }}
    .card {{
      background: #ffffff;
      border: 1px solid #d8d2c8;
      border-radius: 16px;
      padding: 20px;
    }}
    .status {{
      display: inline-block;
      padding: 8px 12px;
      border-radius: 999px;
      background: #d9ead3;
      color: #245c2a;
      font-weight: 700;
    }}
    ul {{
      padding-left: 18px;
    }}
  </style>
</head>
<body>
{id_comment}  <main class="page">
    <section class="hero">
      <h1>{title}</h1>
      <p>{page_intro}</p>
    </section>

    <section class="grid">
{cards.rstrip()}
    </section>
  </main>
</body>
</html>
"""
    return {"html": html}


def flatten_feature_items(feature_list: list[dict[str, object]]) -> list[str]:
    items: list[str] = []
    for level_1 in feature_list:
        items.append(str(level_1["level_1"]))
        for level_2 in level_1["level_2"]:
            items.append(str(level_2["name"]))
            items.extend(str(item) for item in level_2["level_3"])
    return items


def find_duplicate_items(items: list[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for item in items:
        normalized = item.lower()
        if normalized in seen:
            duplicates.add(item)
        seen.add(normalized)
    return sorted(duplicates)


def validate_package(
    raw_text: str,
    ba_package: dict[str, object],
    uxui_package: dict[str, object],
) -> dict[str, list[str] | str]:
    """Create review notes for the BA-led package."""
    lower_text = raw_text.lower()
    ambiguity_issues: list[str] = []
    completeness_issues: list[str] = []
    consistency_issues: list[str] = []
    template_issues: list[str] = []

    ambiguous_terms = {
        "fast": "Replace 'fast' with a measurable speed target.",
        "easy": "Explain what makes the experience easy.",
        "simple": "Describe the exact rule or flow instead of saying 'simple'.",
        "quickly": "Add a target time or service level.",
        "user-friendly": "Describe the expected user behavior or screen outcome.",
    }
    for term, advice in ambiguous_terms.items():
        if term in lower_text:
            ambiguity_issues.append(f"The word '{term}' is vague. {advice}")

    for assumption in ba_package["assumptions"]:
        lower_assumption = str(assumption).lower()
        if "still" in lower_assumption or "may" in lower_assumption:
            ambiguity_issues.append(
                f"An assumption is still open-ended: '{assumption}'. Confirm it before review."
            )

    if not ba_package["business_rules"]:
        completeness_issues.append("Business rules are missing from the BA package.")
    if not str(ba_package["bpmn_mermaid"]).startswith("flowchart"):
        completeness_issues.append("The BPMN Mermaid output is missing or incomplete.")
    if "{" not in str(ba_package["bpmn_mermaid"]):
        completeness_issues.append("The BPMN Mermaid output should include at least one decision point.")
    if len(ba_package["acceptance_criteria"]) < 3:
        completeness_issues.append("Acceptance criteria should include at least three clear points.")
    if ba_package["functional_scope_exists"] and not ba_package["feature_list"]:
        completeness_issues.append(
            "Feature list is missing even though the BA package contains functional scope."
        )
    if not ba_package["frs"]["main_flow"]:
        completeness_issues.append("FRS main flow is missing.")
    if not ba_package["frs"]["alternative_flows"]:
        completeness_issues.append("FRS alternative flows are missing.")
    if not ba_package["frs"]["edge_cases"]:
        completeness_issues.append("FRS edge cases are missing.")
    if not uxui_package["main_sections"]:
        completeness_issues.append("Wireframe output should include main sections.")

    subjective_words = ["should", "easy", "simple", "quick", "user-friendly"]
    observable_words = ["can", "display", "displays", "show", "shows", "prevent", "prevents", "view"]
    for criterion in ba_package["acceptance_criteria"]:
        lower_criterion = str(criterion).lower()
        if any(word in lower_criterion for word in subjective_words):
            consistency_issues.append(
                f"Acceptance criterion is not testable enough: '{criterion}'. Use observable wording."
            )
        if not any(word in lower_criterion for word in observable_words):
            consistency_issues.append(
                f"Acceptance criterion may be too vague for testing: '{criterion}'."
            )
        if not all(word in lower_criterion for word in ["given", "when", "then"]):
            consistency_issues.append(
                f"Acceptance criterion should use Given/When/Then for clarity: '{criterion}'."
            )

    if ba_package["feature_list"]:
        feature_items = flatten_feature_items(ba_package["feature_list"])
        duplicate_features = find_duplicate_items(feature_items)
        for duplicate in duplicate_features:
            consistency_issues.append(
                f"Feature list contains a duplicate or overlapping item: '{duplicate}'."
            )

        feature_text = " ".join(feature_items).lower()
        frs_text = (
            str(ba_package["frs"]["functional_summary"]).lower()
            + " "
            + " ".join(str(item).lower() for item in ba_package["frs"]["business_rules"])
            + " "
            + " ".join(str(item).lower() for item in ba_package["frs"]["edge_cases"])
        )
        for concept in ["status", "support", "booking", "ticket", "loyalty", "points", "tier"]:
            if concept in frs_text and concept not in feature_text:
                consistency_issues.append(
                    f"Feature list may not fully align with the FRS because '{concept}' is missing from the hierarchy."
                )

        for level_1 in ba_package["feature_list"]:
            if not level_1["level_2"]:
                template_issues.append(
                    f"Level 1 feature '{level_1['level_1']}' has no Level 2 features."
                )
            for level_2 in level_1["level_2"]:
                if not level_2["level_3"]:
                    template_issues.append(
                        f"Level 2 feature '{level_2['name']}' has no Level 3 features."
                    )

    if not ba_package["frs"]["business_rules"]:
        template_issues.append("FRS is missing the Business Rules section.")
    if not ba_package["frs"]["edge_cases"]:
        template_issues.append("FRS is missing the Edge Cases section.")

    bpmn_text = str(ba_package["bpmn_mermaid"])
    main_flow_steps = list(ba_package["frs"]["main_flow"])
    alternative_flow_steps = list(ba_package["frs"]["alternative_flows"])

    if main_flow_steps:
        consistency_issues.extend(
            flow_alignment_issues(bpmn_text, main_flow_steps, "main flow")
        )
    if alternative_flow_steps:
        consistency_issues.extend(
            flow_alignment_issues(bpmn_text, alternative_flow_steps, "alternative flow")
        )

    bpmn_lower = bpmn_text.lower()
    if "{" in bpmn_text and not alternative_flow_steps:
        consistency_issues.append(
            "BPMN shows a decision point but FRS has no alternative flows."
        )
    if alternative_flow_steps and "{" not in bpmn_text:
        consistency_issues.append(
            "FRS lists alternative flows but BPMN has no decision points."
        )

    all_issues = ambiguity_issues + completeness_issues + consistency_issues + template_issues
    return {
        "status": "pass" if not all_issues else "needs-review",
        "ambiguity_issues": ambiguity_issues,
        "completeness_issues": completeness_issues,
        "consistency_issues": consistency_issues,
        "template_issues": template_issues,
    }


def format_bullet_list(items: list[str]) -> list[str]:
    if not items:
        return ["- No issues found."]
    return [f"- {item}" for item in items]


def format_feature_list_markdown(
    feature_list: list[dict[str, object]],
    include_header: bool = True,
) -> str:
    lines = ["# Feature Breakdown", ""] if include_header else []
    for level_1 in feature_list:
        lines.append(f"## {level_1['level_1']}")
        lines.append("")
        for level_2 in level_1["level_2"]:
            lines.append(f"### {level_2['name']}")
            lines.append("")
            for item in level_2["level_3"]:
                lines.append(f"#### {item}")
            lines.append("")
    return "\n".join(lines).strip()


def create_markdown_files(
    input_path: Path,
    playbook_name: str,
    ba_package: dict[str, object],
    uxui_package: dict[str, object],
    validation: dict[str, list[str] | str],
    id_map: dict[str, str],
) -> dict[str, str]:
    """Prepare the final Markdown outputs."""
    if ba_package["functional_scope_exists"] and not ba_package["feature_list"]:
        raise ValueError("feature-list.md is required when the BA package contains functional scope.")

    clarification_md = "\n".join(
        [
            f"# Clarification: {ba_package['title']}",
            "",
            f"- Requirement ID: `{id_map['req']}`",
            f"- Project: `{ba_package['project_name']}`",
            f"- Project Owner: `{ba_package['project_owner']}`",
            f"- Domain: `{ba_package['project_domain']}`",
            f"- Input File: `{input_path.name}`",
            "- Agent: `BA Agent`",
            f"- Playbook: `{playbook_name}`",
            f"- Knowledge Priority: `{ba_package['knowledge_priority']}`",
            "",
            "## Summary",
            str(ba_package["summary"]),
            "",
            "## Known Facts",
            *[f"- {item}" for item in ba_package["known_facts"]],
            "",
            "## Assumptions",
            *[f"- {item}" for item in ba_package["assumptions"]],
            "",
            "## Open Questions",
            *[f"- {item}" for item in ba_package["open_questions"]],
            "",
            "## Next Actions",
            *[f"- {item}" for item in ba_package["next_actions"]],
        ]
    )

    process_bpmn_md = "\n".join(
        [
            f"# BPMN Process: {ba_package['title']}",
            "",
            f"- Requirement ID: `{id_map['req']}`",
            "## Mermaid Diagram",
            "```mermaid",
            str(ba_package["bpmn_mermaid"]),
            "```",
        ]
    )

    user_story_md = "\n".join(
        [
            f"# User Story: {ba_package['user_story']['title']}",
            "",
            f"- Story ID: `{id_map['us']}`",
            f"- Parent FR ID: `{id_map['fr']}`",
            f"- Parent REQ ID: `{id_map['req']}`",
            "## Story",
            str(ba_package["user_story"]["story"]),
            "",
            "## Context",
            str(ba_package["user_story"]["context"]),
            "",
            "## INVEST Check",
            *[f"- {item}" for item in ba_package["user_story"]["invest"]],
            "",
            "## Dependencies",
            str(ba_package["user_story"]["dependencies"]),
        ]
    )

    acceptance_criteria_md = "\n".join(
        [
            f"# Acceptance Criteria: {ba_package['title']}",
            "",
            f"- AC ID: `{id_map['ac']}`",
            f"- Parent Story ID: `{id_map['us']}`",
            "## Criteria",
            *[f"- {item}" for item in ba_package["acceptance_criteria"]],
        ]
    )

    brd_md = "\n".join(
        [
            f"# BRD: {ba_package['brd']['title']}",
            "",
            f"- BRD ID: `{id_map['brd']}`",
            f"- Parent REQ ID: `{id_map['req']}`",
            "## Business Problem",
            str(ba_package["brd"]["business_problem"]),
            "",
            "## Business Goals",
            *[f"- {item}" for item in ba_package["brd"]["business_goals"]],
            "",
            "## Stakeholders",
            *[f"- {item}" for item in ba_package["brd"]["stakeholders"]],
            "",
            "## Scope",
            *[f"- {item}" for item in ba_package["brd"]["scope"]],
            "",
            "## Business Rules",
            *[f"- {item}" for item in ba_package["brd"]["business_rules"]],
            "",
            "## Assumptions",
            *[f"- {item}" for item in ba_package["brd"]["assumptions"]],
            "",
            "## Expected Benefits",
            *[f"- {item}" for item in ba_package["brd"]["expected_benefits"]],
        ]
    )

    frs_md = "\n".join(
        [
            f"# FRS: {ba_package['frs']['title']}",
            "",
            f"- FR ID: `{id_map['fr']}`",
            f"- Parent REQ ID: `{id_map['req']}`",
            "## Functional Summary",
            str(ba_package["frs"]["functional_summary"]),
            "",
            "## Actors",
            *[f"- {item}" for item in ba_package["frs"]["actors"]],
            "",
            "## Functional Requirements",
            *[f"- {item}" for item in ba_package["frs"]["functional_requirements"]],
            "",
            "## Main Flow",
            *[f"- {item}" for item in ba_package["frs"]["main_flow"]],
            "",
            "## Alternative Flows",
            *[f"- {item}" for item in ba_package["frs"]["alternative_flows"]],
            "",
            "## Business Rules",
            *[f"- {item}" for item in ba_package["frs"]["business_rules"]],
            "",
            "## Validations",
            *[f"- {item}" for item in ba_package["frs"]["validations"]],
            "",
            "## Edge Cases",
            *[f"- {item}" for item in ba_package["frs"]["edge_cases"]],
            "",
            "## Dependencies",
            *[f"- {item}" for item in ba_package["frs"]["dependencies"]],
            "",
            "## Open Questions",
            *[f"- {item}" for item in ba_package["frs"]["open_questions"]],
        ]
    )

    wireframe_md = "\n".join(
        [
            f"# Wireframe: {uxui_package['title']}",
            "",
            f"- UI ID: `{id_map['ui']}`",
            f"- Parent FR ID: `{id_map['fr']}`",
            f"- Parent FEAT ID: `{id_map['feat']}`",
            "## Primary Input",
            str(uxui_package["primary_input"]),
            "",
            "## Screen Goal",
            str(uxui_package["screen_goal"]),
            "",
            "## Main Sections",
            *[f"- {item}" for item in uxui_package["main_sections"]],
            "",
            "## Components",
            *[f"- {item}" for item in uxui_package["components"]],
            "",
            "## Interaction Notes",
            *[f"- {item}" for item in uxui_package["interaction_notes"]],
            "",
            "## Wireframe Sketch",
            "```text",
            str(uxui_package["wireframe_sketch"]),
            "```",
        ]
    )

    knowledge_context_md = [
        "## Knowledge Context",
        f"- Global context files loaded: {', '.join(ba_package['global_context_files_loaded']) or 'None'}",
        f"- Project context files loaded: {', '.join(ba_package['project_context_files_loaded']) or 'None'}",
        f"- Project knowledge files loaded: {', '.join(ba_package['project_files_loaded']) or 'None'}",
        f"- Shared knowledge files loaded: {', '.join(ba_package['shared_files_loaded']) or 'None'}",
        f"- Business rules source: {ba_package['business_rule_source']}",
    ]

    review_notes_md = "\n".join(
        [
            "# Review Notes",
            "",
            f"- Review ID: `{id_map['rv']}`",
            f"- Parent REQ ID: `{id_map['req']}`",
            f"- Project: `{ba_package['project_name']}`",
            f"- Input File: `{input_path.name}`",
            f"- Playbook: `{playbook_name}`",
            "- Agent Flow: `BA -> UXUI -> FE -> Reviewer`",
            f"- Validation Status: `{validation['status']}`",
            "",
            *knowledge_context_md,
            "",
            "## Ambiguity Checker",
            *format_bullet_list(validation["ambiguity_issues"]),
            "",
            "## Completeness Checker",
            *format_bullet_list(validation["completeness_issues"]),
            "",
            "## Consistency Checker",
            *format_bullet_list(validation["consistency_issues"]),
            "",
            "## Template Checker",
            *format_bullet_list(validation["template_issues"]),
            "",
            "## Suggested Next Step",
            "- Review the BA package first, then confirm the wireframe and HTML against the BA FRS.",
        ]
    )

    return {
        "clarification.md": clarification_md,
        "process-bpmn.md": process_bpmn_md,
        "user-story.md": user_story_md,
        "acceptance-criteria.md": acceptance_criteria_md,
        "brd.md": brd_md,
        "frs.md": frs_md,
        "feature-list.md": "\n".join(
            [
                "# Feature Breakdown",
                "",
                f"- Feature ID: `{id_map['feat']}`",
                f"- Parent FR ID: `{id_map['fr']}`",
                "",
                format_feature_list_markdown(ba_package["feature_list"], include_header=False),
            ]
        ),
        "wireframe.md": wireframe_md,
        "review-notes.md": review_notes_md,
    }


def remove_old_demo_files(output_folder: Path) -> None:
    """Remove older filenames from previous demo versions."""
    old_filenames = [
        "mini-prd.md",
        "bpmn-process.md",
        "feature-breakdown.md",
        "order-status-page.html",
    ]
    for filename in old_filenames:
        old_file = output_folder / filename
        if old_file.exists():
            old_file.unlink()


def sync_curated_outputs(project_dir: Path, requirement_name: str) -> None:
    """Copy key outputs to a clean user-facing surface under 02-output/."""
    output_folder = project_paths.requirement_output_dir(project_dir, requirement_name)
    curated_ba = project_paths.curated_ba_dir(project_dir)
    curated_design = project_paths.curated_design_dir(project_dir)
    curated_fe = project_paths.curated_fe_dir(project_dir)
    for folder in [curated_ba, curated_design, curated_fe]:
        folder.mkdir(parents=True, exist_ok=True)

    requirement_header = f"# Requirement: {requirement_name}\n\n"
    mapping = [
        ("clarification.md", curated_ba),
        ("brd.md", curated_ba),
        ("frs.md", curated_ba),
        ("user-story.md", curated_ba),
        ("acceptance-criteria.md", curated_ba),
        ("feature-list.md", curated_ba),
        ("process-bpmn.md", curated_ba),
        ("process-bpmn.md", curated_design),
        ("wireframe.md", curated_design),
        ("ui.html", curated_fe),
    ]
    for file_name, target_dir in mapping:
        source = output_folder / file_name
        if not source.exists():
            continue
        target = target_dir / f"{requirement_name}-{file_name}"
        if file_name.endswith(".md"):
            content = source.read_text(encoding="utf-8").strip()
            target.write_text(requirement_header + content + "\n", encoding="utf-8")
        else:
            target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")

def list_projects(selected_project: str | None = None) -> list[Path]:
    """Return valid project folders under projects/."""
    projects: list[Path] = []
    for entry in sorted(PROJECTS_DIR.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name.startswith(".") or entry.name == "project-template":
            continue
        if (entry / "project-config.yaml").exists():
            if selected_project and entry.name != selected_project:
                continue
            projects.append(entry)
    if selected_project and not projects:
        raise FileNotFoundError(f"Project '{selected_project}' was not found.")
    return projects


def list_requirement_inputs(project_dir: Path) -> list[Path]:
    """List requirement inputs for one project."""
    requirements_dir = project_paths.requirements_dir(project_dir)
    if not requirements_dir.exists():
        return []
    return sorted(path for path in requirements_dir.iterdir() if path.is_file())


def output_folder_exists(project_dir: Path, requirement_name: str) -> bool:
    return project_paths.requirement_output_dir(project_dir, requirement_name).exists()


def _prepare_generation_context(
    project_dir: Path,
    input_file: Path,
    project_config: dict[str, object],
) -> dict[str, object]:
    """Build one generation context that can be reused in full or controlled mode."""
    requirement_name = input_file.stem
    project_name = project_dir.name

    id_manager = load_local_module("id_manager", "system/tools/project/id_manager.py")
    id_map = id_manager.get_or_create_ids(project_dir, input_file)
    id_manager.ensure_requirement_id_header(input_file, id_map["req"])

    raw_text = reader.read_text_file(input_file)
    scenario_manager = load_local_module("scenario_manager", "system/tools/project/scenario_manager.py")
    scenario_context = scenario_manager.resolve_project_scenario(BASE_DIR, project_config)
    log_step("SCENARIO", f"{project_name}: {scenario_manager.describe_scenario_resolution(scenario_context)}")
    context_loader = load_local_module("context_loader", "system/tools/context/context_loader.py")
    prompt_builder = load_local_module("prompt_builder", "system/tools/context/prompt_builder.py")
    auto_context = context_loader.build_full_context(project_name)
    context_package = prompt_builder.build_prompt_package(
        global_context=str(auto_context.get("global_text", "")),
        project_context=str(auto_context.get("project_text", "")),
        task_input=raw_text,
    )
    auto_context["text"] = context_package
    log_context_load(
        project_name=project_name,
        global_loaded=list(auto_context.get("global_loaded_files", [])),
        global_missing=list(auto_context.get("global_missing_files", [])),
        project_loaded=list(auto_context.get("project_loaded_files", [])),
        project_missing=list(auto_context.get("project_missing_files", [])),
    )

    knowledge_bundle = load_knowledge_bundle(project_dir, auto_context=auto_context)
    ba_package = build_ba_package(raw_text, project_config, knowledge_bundle, scenario_context)
    uxui_package = build_uxui_package(ba_package)
    fe_package = build_fe_package(ba_package, uxui_package, id_map)
    validation = validate_package(raw_text, ba_package, uxui_package)

    playbook_folder_name = str(project_config.get("default_playbook", "product-development"))
    playbook_file = BASE_DIR / "system" / "playbooks" / playbook_folder_name / "playbook.yaml"
    playbook_name = read_playbook_name(playbook_file)

    markdown_files = create_markdown_files(
        input_file,
        playbook_name,
        ba_package,
        uxui_package,
        validation,
        id_map,
    )
    html_files = {"ui.html": fe_package["html"]}

    output_folder = writer.create_project_output_folder(project_dir, requirement_name)
    remove_old_demo_files(output_folder)

    test_case_manager = load_local_module("test_case_manager", "system/tools/project/test_case_manager.py")
    test_cases_md, tc_ids = test_case_manager.generate_test_cases(
        project_dir=project_dir,
        project_name=project_name,
        requirement_name=requirement_name,
        ids=id_map,
        ba_package=ba_package,
        id_manager_module=id_manager,
        output_dir=output_folder,
    )
    markdown_files["test-cases.md"] = test_cases_md

    return {
        "project_name": project_name,
        "requirement_name": requirement_name,
        "id_map": id_map,
        "output_folder": output_folder,
        "markdown_files": markdown_files,
        "html_files": html_files,
        "tc_ids": tc_ids,
    }


def _post_generation_updates(
    project_dir: Path,
    input_file: Path,
    project_config: dict[str, object],
    generation: dict[str, object],
    markdown_written: dict[str, str],
    html_written: dict[str, str],
    changed_artifacts: list[str],
    is_new_output: bool,
    reason: str,
) -> None:
    """Update versioning, status, traceability, and flow files after generation."""
    requirement_name = str(generation["requirement_name"])
    project_name = str(generation["project_name"])
    id_map = generation["id_map"]
    output_folder = Path(generation["output_folder"])
    tc_ids = [str(item) for item in generation.get("tc_ids", [])]

    version_manager = load_local_module("version_manager", "system/tools/project/version_manager.py")

    affected_ids = unique_items(
        [
            id_map.get("req", ""),
            id_map.get("brd", ""),
            id_map.get("fr", ""),
            id_map.get("us", ""),
            id_map.get("ac", ""),
            id_map.get("feat", ""),
            id_map.get("ui", ""),
            id_map.get("rv", ""),
            *tc_ids,
        ]
    )
    affected_ids = [item for item in affected_ids if item]
    version_result = version_manager.update_version_tracking(
        project_dir=project_dir,
        output_dir=output_folder,
        requirement_name=requirement_name,
        requirement_id=id_map["req"],
        changed_artifacts=changed_artifacts,
        affected_ids=affected_ids,
        is_new_output=is_new_output,
        reason=reason,
    )
    log_step(
        "VERSION",
        (
            f"{project_name}/{requirement_name} -> version {version_result.get('current_version')} "
            f"(changed: {', '.join(version_result.get('changed_artifacts', [])) or 'none'})"
        ),
    )

    # Status update should reflect what is currently on disk, not only current write set.
    ba_outputs = [
        "clarification.md",
        "process-bpmn.md",
        "user-story.md",
        "acceptance-criteria.md",
        "brd.md",
        "frs.md",
        "feature-list.md",
    ]
    ba_done = all((output_folder / name).exists() for name in ba_outputs)
    uxui_done = (output_folder / "wireframe.md").exists()
    fe_done = (output_folder / "ui.html").exists()
    reviewer_done = (output_folder / "review-notes.md").exists()
    project_owner = str(project_config.get("owner", "BA Team"))

    # TODO: Expand status updates to include blockers and next actions when available.
    status_manager.update_project_status(
        project_dir=project_dir,
        project_name=project_name,
        owner=project_owner,
        requirement_name=requirement_name,
        ba_done=ba_done,
        uxui_done=uxui_done,
        fe_done=fe_done,
        reviewer_done=reviewer_done,
        notes="Auto-updated after output generation.",
    )
    log_step(
        "STATUS",
        status_manager.describe_status_update(
            project_name=project_name,
            requirement_name=requirement_name,
            ba_done=ba_done,
            uxui_done=uxui_done,
            fe_done=fe_done,
            reviewer_done=reviewer_done,
        ),
    )

    requirement_flow_manager = load_local_module(
        "requirement_flow_manager", "system/tools/project/requirement_flow_manager.py"
    )
    requirement_flow_manager.write_requirement_flow(
        project_dir=project_dir,
        requirement_name=requirement_name,
        input_file=input_file,
        requirement_id=id_map["req"],
    )
    log_step("FLOW", f"{project_name}/{requirement_name}: requirement flow refreshed.")

    if (
        "requirement-traceability-matrix.md" in markdown_written
        or "requirement-traceability-flow.md" in markdown_written
    ):
        traceability_manager = load_local_module(
            "traceability_manager", "system/tools/project/traceability_manager.py"
        )
        traceability_paths = traceability_manager.write_requirement_traceability(
            project_dir=project_dir,
            requirement_name=requirement_name,
            input_file=input_file,
            requirement_id=id_map["req"],
            tc_ids=tc_ids,
        )
        log_step(
            "TRACE",
            f"{project_name}/{requirement_name}: requirement traceability refreshed ({len(traceability_paths)} files).",
        )

    sync_curated_outputs(project_dir, requirement_name)


def _normalize_artifact_name(name: str) -> str:
    value = name.strip().lower()
    mapping = {
        "clarification": "clarification",
        "clarification.md": "clarification",
        "brd": "brd",
        "brd.md": "brd",
        "process-bpmn": "process-bpmn",
        "process-bpmn.md": "process-bpmn",
        "bpmn": "process-bpmn",
        "frs": "frs",
        "frs.md": "frs",
        "user-story": "user-story",
        "user-story.md": "user-story",
        "acceptance-criteria": "acceptance-criteria",
        "acceptance-criteria.md": "acceptance-criteria",
        "feature-list": "feature-list",
        "feature-list.md": "feature-list",
        "wireframe": "wireframe",
        "wireframe.md": "wireframe",
        "ui": "ui",
        "ui.html": "ui",
        "review": "review",
        "review-notes.md": "review",
        "test-cases": "test-cases",
        "test-cases.md": "test-cases",
        "requirement-traceability-matrix": "requirement-traceability-matrix",
        "requirement-traceability-matrix.md": "requirement-traceability-matrix",
        "requirement-traceability-flow": "requirement-traceability-flow",
        "requirement-traceability-flow.md": "requirement-traceability-flow",
        "risk-notes": "risk-notes",
        "risk-notes.md": "risk-notes",
        "dependency-map": "dependency-map",
        "dependency-map.md": "dependency-map",
    }
    return mapping.get(value, value)


def _build_risk_notes_markdown(
    project_dir: Path,
    project_name: str,
    requirement_name: str,
    requirement_id: str,
    output_folder: Path,
) -> str:
    review_text = reader.read_text_if_exists(output_folder / "review-notes.md")
    dependency_text = reader.read_text_if_exists(project_paths.dependency_map_path(project_dir))
    risks: list[str] = []

    if "needs-review" in review_text.lower():
        risks.append("Review notes show unresolved quality issues.")
    if "Missing:" in review_text:
        risks.append("Some required sections or files are marked as missing.")
    if "No high dependency risk detected" not in dependency_text and dependency_text.strip():
        risks.append("Dependency map contains active downstream dependency risk.")
    if not risks:
        risks.append("No critical risk detected from current review and dependency artifacts.")

    lines = [
        "# Risk Notes",
        "",
        "## Overview",
        f"- Project Name: {project_name}",
        f"- Requirement Name: {requirement_name}",
        f"- Requirement ID: {requirement_id}",
        "",
        "## Key Risks",
    ]
    for risk in risks:
        lines.append(f"- {risk}")
    lines.extend(
        [
            "",
            "## Suggested Mitigations",
            "- Resolve warnings in review notes before stakeholder sign-off.",
            "- Re-check dependency-map after major BA output updates.",
            "",
            "<!-- TODO: Add severity labels (High/Medium/Low) for each risk line. -->",
            "",
        ]
    )
    return "\n".join(lines)


def run_pipeline_for_input(
    project_dir: Path,
    input_file: Path,
    project_config: dict[str, object],
    force: bool,
    mode: str = "full",
    artifact: str | None = None,
    stage: str | None = None,
    override_gate: bool = False,
) -> bool:
    requirement_name = input_file.stem
    project_name = project_dir.name

    already_processed = output_folder_exists(project_dir, requirement_name)

    try:
        log_step("PROJECT", project_name)
        log_step("INPUT", f"{input_file.name} ({mode})")
        log_info(f"Requirement {requirement_name} started.")
        generation = _prepare_generation_context(project_dir, input_file, project_config)
        id_map = generation["id_map"]
        output_folder = Path(generation["output_folder"])
        markdown_files = generation["markdown_files"]
        html_files = generation["html_files"]
        version_manager = load_local_module("version_manager", "system/tools/project/version_manager.py")
        artifact_runner = load_local_module("artifact_runner", "system/tools/project/artifact_runner.py")
        artifact_review_manager = load_local_module(
            "artifact_review_manager", "system/tools/project/artifact_review_manager.py"
        )
        dependency_manager = load_local_module("dependency_manager", "system/tools/project/dependency_manager.py")
        traceability_manager = load_local_module(
            "traceability_manager", "system/tools/project/traceability_manager.py"
        )

        catalog = artifact_runner.load_artifact_catalog(ARTIFACT_CATALOG_PATH)
        catalog_index = artifact_runner.catalog_by_name(catalog)
        gates_config = artifact_runner.load_gates_config(GATES_CONFIG_PATH)
        artifact_runner.ensure_artifact_status(
            project_dir=project_dir,
            requirement_name=requirement_name,
            requirement_id=id_map["req"],
            catalog=catalog,
        )
        artifact_runner.ensure_artifact_checklist(
            project_dir=project_dir,
            requirement_name=requirement_name,
            requirement_id=id_map["req"],
            catalog=catalog,
        )
        artifact_review_manager.ensure_artifact_reviews(
            project_dir=project_dir,
            requirement_name=requirement_name,
            requirement_id=id_map["req"],
            catalog=catalog,
            checklist_templates_dir=CHECKLIST_TEMPLATES_DIR,
        )
        log_step(
            "GOVERNANCE",
            f"{project_name}/{requirement_name}: artifact status/checklist/reviews ready.",
        )

        target_artifact = _normalize_artifact_name(artifact) if artifact else None
        target_stage = stage.strip() if stage else None
        execution_plan = artifact_runner.build_execution_plan(
            catalog=catalog,
            target_artifact=target_artifact,
            target_stage=target_stage,
        )

        markdown_written: dict[str, str] = {}
        html_written: dict[str, str] = {}
        gate_results = artifact_runner.parse_gate_results(project_dir, requirement_name)

        for artifact_name in execution_plan:
            artifact_state = artifact_runner.parse_artifact_status(project_dir, requirement_name, catalog)
            artifact_definition = catalog_index.get(artifact_name, {})
            artifact_stage = str(artifact_definition.get("stage", "")).strip() or "stage"
            artifact_owner = str(artifact_definition.get("owner", "")).strip().replace("-agent", "").upper()
            step_scope = f"{artifact_owner}/{artifact_stage}"
            log_step(step_scope, f"Running artifact: {artifact_name}")

            if (
                artifact_state.get(artifact_name, {}).get("status") == "Done"
                and artifact_state.get(artifact_name, {}).get("gate") == "Pass"
                and not force
            ):
                skip_row = artifact_state.get(artifact_name, {})
                skip_rule = gates_config.get(
                    artifact_name,
                    {"allow_downstream_if": ["Pass"], "allow_approval_if": ["Approved", "In Review"]},
                )
                skip_downstream_allowed = (
                    skip_row.get("gate", "N/A") in skip_rule.get("allow_downstream_if", ["Pass"])
                    and skip_row.get("approval", "Draft")
                    in skip_rule.get("allow_approval_if", ["Approved", "In Review"])
                )
                artifact_runner.update_gate_result_row(
                    gate_results=gate_results,
                    artifact_name=artifact_name,
                    validation_result="Not Run",
                    gate_result="Pass",
                    downstream_allowed=skip_downstream_allowed,
                    reason="Skipped because artifact already passed and --force was not used.",
                )
                artifact_review_manager.update_artifact_review(
                    project_dir=project_dir,
                    requirement_name=requirement_name,
                    requirement_id=id_map["req"],
                    artifact_name=artifact_name,
                    approval_state=skip_row.get("approval", "Approved"),
                    gate_result=skip_row.get("gate", "Pass"),
                    notes="Skipped: existing artifact already meets run criteria.",
                    checklist_templates_dir=CHECKLIST_TEMPLATES_DIR,
                )
                log_skipped(
                    f"{project_name}/{input_file.name} -> {artifact_name} skipped (already passed)."
                )
                continue

            can_run, issues = artifact_runner.check_dependencies(
                artifact_name=artifact_name,
                catalog_index=catalog_index,
                state=artifact_state,
                gates_config=gates_config,
                override_gate=override_gate,
            )
            if not can_run:
                artifact_runner.set_blocked(artifact_state, artifact_name, issues)
                artifact_runner.write_artifact_status(
                    project_dir, requirement_name, id_map["req"], catalog, artifact_state
                )
                blocked_row = artifact_state.get(artifact_name, {})
                artifact_review_manager.update_artifact_review(
                    project_dir=project_dir,
                    requirement_name=requirement_name,
                    requirement_id=id_map["req"],
                    artifact_name=artifact_name,
                    approval_state=blocked_row.get("approval", "Blocked"),
                    gate_result=blocked_row.get("gate", "Not Allowed"),
                    notes=blocked_row.get("notes", "Blocked by gate/dependency."),
                    checklist_templates_dir=CHECKLIST_TEMPLATES_DIR,
                )
                artifact_runner.update_gate_result_row(
                    gate_results=gate_results,
                    artifact_name=artifact_name,
                    validation_result="Not Run",
                    gate_result="Not Allowed",
                    downstream_allowed=False,
                    reason="; ".join(issues) if issues else "Blocked by dependency gate rules.",
                )
                log_blocked(
                    f"{project_name}/{input_file.name} -> {artifact_name} blocked: "
                    + ("; ".join(issues) if issues else "dependency gate not satisfied")
                )
                if mode == "controlled":
                    artifact_runner.write_gate_results(
                        project_dir=project_dir,
                        requirement_name=requirement_name,
                        requirement_id=id_map["req"],
                        catalog=catalog,
                        gate_results=gate_results,
                    )
                    artifact_runner.write_gate_report(
                        project_dir=project_dir,
                        requirement_name=requirement_name,
                        requirement_id=id_map["req"],
                        catalog=catalog,
                        state=artifact_state,
                    )
                    log_step(
                        "GATE",
                        (
                            f"{project_name}/{requirement_name}: blocked by upstream gate for {artifact_name} "
                            f"({'; '.join(issues) if issues else 'dependency rules'})"
                        ),
                    )
                    return False
                continue
            dependency_override_note = ""
            if override_gate and issues:
                dependency_override_note = "; ".join(issues)

            artifact_runner.set_in_progress(artifact_state, artifact_name)
            artifact_runner.write_artifact_status(
                project_dir, requirement_name, id_map["req"], catalog, artifact_state
            )

            generated_content = ""
            if artifact_name == "clarification":
                generated_content = str(markdown_files["clarification.md"])
                writer.write_markdown_file(output_folder, "clarification.md", generated_content)
                markdown_written["clarification.md"] = generated_content
            elif artifact_name == "brd":
                generated_content = str(markdown_files["brd.md"])
                writer.write_markdown_file(output_folder, "brd.md", generated_content)
                markdown_written["brd.md"] = generated_content
            elif artifact_name == "process-bpmn":
                generated_content = str(markdown_files["process-bpmn.md"])
                writer.write_markdown_file(output_folder, "process-bpmn.md", generated_content)
                markdown_written["process-bpmn.md"] = generated_content
            elif artifact_name == "frs":
                generated_content = str(markdown_files["frs.md"])
                writer.write_markdown_file(output_folder, "frs.md", generated_content)
                markdown_written["frs.md"] = generated_content
            elif artifact_name == "user-story":
                generated_content = str(markdown_files["user-story.md"])
                writer.write_markdown_file(output_folder, "user-story.md", generated_content)
                markdown_written["user-story.md"] = generated_content
            elif artifact_name == "acceptance-criteria":
                generated_content = str(markdown_files["acceptance-criteria.md"])
                writer.write_markdown_file(output_folder, "acceptance-criteria.md", generated_content)
                markdown_written["acceptance-criteria.md"] = generated_content
            elif artifact_name == "feature-list":
                generated_content = str(markdown_files["feature-list.md"])
                writer.write_markdown_file(output_folder, "feature-list.md", generated_content)
                markdown_written["feature-list.md"] = generated_content
            elif artifact_name == "wireframe":
                generated_content = str(markdown_files["wireframe.md"])
                writer.write_markdown_file(output_folder, "wireframe.md", generated_content)
                markdown_written["wireframe.md"] = generated_content
            elif artifact_name == "ui":
                generated_content = str(html_files["ui.html"])
                writer.write_html_file(output_folder, "ui.html", generated_content)
                html_written["ui.html"] = generated_content
            elif artifact_name == "review":
                generated_content = str(markdown_files["review-notes.md"])
                writer.write_markdown_file(output_folder, "review-notes.md", generated_content)
                markdown_written["review-notes.md"] = generated_content
            elif artifact_name == "test-cases":
                generated_content = str(markdown_files["test-cases.md"])
                writer.write_markdown_file(output_folder, "test-cases.md", generated_content)
                markdown_written["test-cases.md"] = generated_content
            elif artifact_name == "requirement-traceability-matrix":
                generated_content = traceability_manager.build_requirement_traceability_matrix(
                    project_dir=project_dir,
                    requirement_name=requirement_name,
                    input_file=input_file,
                    requirement_id=id_map["req"],
                    tc_ids=generation["tc_ids"],
                )
                writer.write_markdown_file(
                    output_folder, "requirement-traceability-matrix.md", generated_content
                )
                markdown_written["requirement-traceability-matrix.md"] = generated_content
            elif artifact_name == "requirement-traceability-flow":
                generated_content = traceability_manager.build_requirement_traceability_flow(
                    project_dir=project_dir,
                    requirement_name=requirement_name,
                    input_file=input_file,
                    requirement_id=id_map["req"],
                    tc_ids=generation["tc_ids"],
                )
                writer.write_markdown_file(
                    output_folder, "requirement-traceability-flow.md", generated_content
                )
                markdown_written["requirement-traceability-flow.md"] = generated_content
            elif artifact_name == "dependency-map":
                dep_path = dependency_manager.write_dependency_map(project_dir)
                generated_content = reader.read_text_file(dep_path)
            elif artifact_name == "risk-notes":
                generated_content = _build_risk_notes_markdown(
                    project_dir=project_dir,
                    project_name=project_name,
                    requirement_name=requirement_name,
                    requirement_id=id_map["req"],
                    output_folder=output_folder,
                )
                writer.write_markdown_file(output_folder, "risk-notes.md", generated_content)
                markdown_written["risk-notes.md"] = generated_content
            else:
                raise ValueError(f"Unsupported artifact implementation: {artifact_name}")

            validators_raw = artifact_definition.get("validators", [])
            validators = [str(item).strip() for item in validators_raw] if isinstance(validators_raw, list) else []
            validation_result, gate_result, gate_note = artifact_runner.detect_gate(
                artifact_name,
                generated_content,
                validators=validators,
            )
            if dependency_override_note:
                gate_note = f"{gate_note}; {dependency_override_note}"
            artifact_runner.set_result(
                artifact_state,
                artifact_name,
                gate_result,
                gate_note,
                override_used=bool(dependency_override_note),
            )
            artifact_runner.write_artifact_status(
                project_dir, requirement_name, id_map["req"], catalog, artifact_state
            )
            result_row = artifact_state.get(artifact_name, {})
            artifact_state_text = artifact_runner.describe_artifact_state(
                artifact_name=artifact_name,
                status=str(result_row.get("status", "")),
                gate_result=gate_result,
                approval_state=str(result_row.get("approval", "")),
            )
            artifact_review_manager.update_artifact_review(
                project_dir=project_dir,
                requirement_name=requirement_name,
                requirement_id=id_map["req"],
                artifact_name=artifact_name,
                approval_state=result_row.get("approval", "Draft"),
                gate_result=gate_result,
                notes=gate_note,
                checklist_templates_dir=CHECKLIST_TEMPLATES_DIR,
            )
            gate_rule = gates_config.get(
                artifact_name,
                {"allow_downstream_if": ["Pass"], "allow_approval_if": ["Approved", "In Review"]},
            )
            allowed_states = gate_rule.get("allow_downstream_if", ["Pass"])
            allowed_approvals = gate_rule.get("allow_approval_if", ["Approved", "In Review"])
            downstream_allowed = gate_result in allowed_states and result_row.get(
                "approval", "Draft"
            ) in allowed_approvals
            artifact_runner.update_gate_result_row(
                gate_results=gate_results,
                artifact_name=artifact_name,
                validation_result=validation_result,
                gate_result=gate_result,
                downstream_allowed=downstream_allowed,
                reason=gate_note,
            )
            if gate_result == "Pass":
                log_success(f"{project_name}/{input_file.name} -> {artifact_state_text}")
            elif gate_result == "Warning":
                log_warning(
                    f"{project_name}/{input_file.name} -> {artifact_state_text} | note={gate_note}"
                )
            else:
                log_blocked(
                    f"{project_name}/{input_file.name} -> {artifact_state_text} | note={gate_note}"
                )

        final_state = artifact_runner.parse_artifact_status(project_dir, requirement_name, catalog)
        artifact_runner.write_gate_results(
            project_dir=project_dir,
            requirement_name=requirement_name,
            requirement_id=id_map["req"],
            catalog=catalog,
            gate_results=gate_results,
        )
        artifact_runner.write_gate_report(
            project_dir=project_dir,
            requirement_name=requirement_name,
            requirement_id=id_map["req"],
            catalog=catalog,
            state=final_state,
        )
        log_step("GATE", f"{project_name}/{requirement_name}: gate results/report refreshed.")

        changed_artifacts = version_manager.detect_artifact_changes(
            output_dir=output_folder,
            markdown_files=markdown_written,
            html_files=html_written,
        )
        _post_generation_updates(
            project_dir=project_dir,
            input_file=input_file,
            project_config=project_config,
            generation=generation,
            markdown_written=markdown_written,
            html_written=html_written,
            changed_artifacts=changed_artifacts,
            is_new_output=not already_processed,
            reason=f"{mode} run artifact update",
        )

        message = f"{project_name}/{input_file.name}: completed ({mode})."
        log_success(message)
        return True
    except Exception as error:
        message = f"Requirement {project_name}/{input_file.name} failed: {error}"
        log_error(message)
        return False


def main() -> None:
    configure_logging()
    args = parse_arguments()
    console_logger.section("2B Agents Pipeline")
    if args.sync_context:
        log_step("CONTEXT", "Running Level 1 context sync...")
        context_sync = load_local_module("context_sync", "system/tools/context/context_sync.py")
        sync_result = context_sync.run_level1_sync(BASE_DIR)
        log_success("Context sync completed.")
        log_info(f"Report: {sync_result.get('report_path')}")
        return

    if (args.artifact or args.stage) and args.mode == "full":
        args.mode = "controlled"
    selected_requirement = args.requirement or args.input

    if args.dashboard:
        log_step("DASHBOARD", "Refreshing dashboard only...")
        dashboard_manager = load_local_module("dashboard_manager", "system/tools/project/dashboard_manager.py")
        dashboard_path = dashboard_manager.write_dashboard(PROJECTS_DIR, WORKSPACE_DIR)
        html_path = dashboard_manager.write_dashboard_html(PROJECTS_DIR, WORKSPACE_DIR)
        log_success(f"Dashboard updated: {dashboard_path}")
        log_success(f"HTML dashboard generated: {html_path}")
        return

    projects = list_projects(args.project)
    input_state_manager = load_local_module(
        "input_state_manager", "system/tools/project/input_state_manager.py"
    )
    run_summary = {
        "projects_processed": 0,
        "requirements_processed": 0,
        "new_inputs": 0,
        "changed_inputs": 0,
        "forced_inputs": 0,
        "unchanged_skipped": 0,
        "failed_items": 0,
    }

    if args.artifact and args.stage:
        raise ValueError("Use either --artifact or --stage, not both.")

    for project_dir in projects:
        console_logger.section(f"Project: {project_dir.name}")
        run_summary["projects_processed"] += 1
        project_config = reader.read_simple_yaml_file(project_dir / "project-config.yaml")
        version_manager = load_local_module("version_manager", "system/tools/project/version_manager.py")
        version_manager.ensure_project_change_log(project_dir)
        input_files = list_requirement_inputs(project_dir)
        processing_state = input_state_manager.load_processing_state(project_dir)
        summary_rows: list[list[str]] = []

        if selected_requirement:
            input_files = [path for path in input_files if path.name == selected_requirement]
            if not input_files:
                message = f"{project_dir.name}: input not found ({selected_requirement})"
                log_skipped(message)
                continue

        if not input_files:
            message = f"{project_dir.name}: no requirement inputs"
            log_skipped(message)
            continue

        for input_file in input_files:
            input_classification = "forced"
            current_hash = input_state_manager.compute_input_hash(input_file)
            if not args.force:
                input_classification, current_hash = input_state_manager.classify_requirement_input(
                    processing_state, input_file
                )

            if input_classification == "new":
                run_summary["new_inputs"] += 1
                log_info(input_state_manager.describe_input_classification(input_file.name, "new"))
            elif input_classification == "changed":
                run_summary["changed_inputs"] += 1
                log_info(input_state_manager.describe_input_classification(input_file.name, "changed"))
            elif input_classification == "unchanged":
                run_summary["unchanged_skipped"] += 1
                log_skipped(input_state_manager.describe_input_classification(input_file.name, "unchanged"))
                summary_rows.append([input_file.name, "unchanged", "skipped"])
                continue
            else:
                run_summary["forced_inputs"] += 1
                log_info(input_state_manager.describe_input_classification(input_file.name, "forced"))

            run_ok = run_pipeline_for_input(
                project_dir=project_dir,
                input_file=input_file,
                project_config=project_config,
                force=args.force,
                mode=args.mode,
                artifact=args.artifact,
                stage=args.stage,
                override_gate=args.override_gate,
            )
            if run_ok:
                run_summary["requirements_processed"] += 1
                output_version = input_state_manager.read_output_version(project_dir, input_file.stem)
                input_state_manager.update_requirement_state(
                    project_dir=project_dir,
                    state=processing_state,
                    file_name=input_file.name,
                    input_hash=current_hash,
                    output_version=output_version,
                    status="processed",
                )
                summary_rows.append([input_file.name, input_classification, "processed"])
            else:
                run_summary["failed_items"] += 1
                summary_rows.append([input_file.name, input_classification, "failed"])
                log_error(f"Requirement {input_file.name} failed for project {project_dir.name}.")

        project_flow_manager = load_local_module(
            "project_flow_manager", "system/tools/project/project_flow_manager.py"
        )
        project_flow_manager.write_project_flow(project_dir)

        traceability_manager = load_local_module(
            "traceability_manager", "system/tools/project/traceability_manager.py"
        )
        traceability_manager.write_project_traceability_summary(project_dir)

        dependency_manager = load_local_module(
            "dependency_manager", "system/tools/project/dependency_manager.py"
        )
        dependency_manager.write_dependency_map(project_dir)
        log_step("OPS", f"{project_dir.name}: project flow, traceability summary, and dependency map refreshed.")
        if summary_rows:
            console_logger.simple_table(
                title=f"Input Processing Summary: {project_dir.name}",
                headers=["Requirement", "Detected", "Result"],
                rows=summary_rows,
            )

    # Auto update dashboard after processing
    dashboard_manager = load_local_module("dashboard_manager", "system/tools/project/dashboard_manager.py")
    dashboard_path = dashboard_manager.write_dashboard(PROJECTS_DIR, WORKSPACE_DIR)
    html_path = dashboard_manager.write_dashboard_html(PROJECTS_DIR, WORKSPACE_DIR)
    log_success(f"Dashboard updated: {dashboard_path}")
    log_success(f"HTML dashboard generated: {html_path}")

    summary_items = [
        ("Processed Projects", str(run_summary["projects_processed"])),
        ("Processed Requirements", str(run_summary["requirements_processed"])),
        ("New Inputs", str(run_summary["new_inputs"])),
        ("Changed Inputs", str(run_summary["changed_inputs"])),
        ("Forced Inputs", str(run_summary["forced_inputs"])),
        ("Skipped Unchanged", str(run_summary["unchanged_skipped"])),
        ("Failed Items", str(run_summary["failed_items"])),
    ]
    if hasattr(console_logger, "summary"):
        console_logger.summary("Run Summary", summary_items)
    else:
        console_logger.section("Run Summary")
        for key, value in summary_items:
            console_logger.info(f"{key}: {value}")


if __name__ == "__main__":
    # TODO: Allow a simple project picker when the user does not pass --project.
    try:
        main()
    except (FileNotFoundError, ValueError) as error:
        log_error(str(error))
        sys.exit(1)
