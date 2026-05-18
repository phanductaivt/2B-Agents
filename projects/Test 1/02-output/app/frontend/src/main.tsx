import React, { FormEvent, useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

type Product = {
  id: string;
  productCode: string;
  productName: string;
  description: string;
  unit: string;
  quantity: number;
  minimumStock: number | null;
  status: "ACTIVE" | "LOW_STOCK" | "OUT_OF_STOCK";
  createdAt: string;
  updatedAt: string;
};

type ProductForm = {
  productCode: string;
  productName: string;
  description: string;
  unit: string;
  quantity: number;
  minimumStock: string;
};

const API_BASE = import.meta.env.VITE_API_BASE ?? "http://127.0.0.1:8000";

const emptyForm: ProductForm = {
  productCode: "",
  productName: "",
  description: "",
  unit: "cái",
  quantity: 0,
  minimumStock: ""
};

function toForm(product: Product): ProductForm {
  return {
    productCode: product.productCode,
    productName: product.productName,
    description: product.description,
    unit: product.unit,
    quantity: product.quantity,
    minimumStock: product.minimumStock === null ? "" : String(product.minimumStock)
  };
}

async function parseResponse<T>(response: Response): Promise<T> {
  const body = await response.json();
  if (!response.ok) {
    throw new Error(body.detail?.message ?? "Thao tác không thành công");
  }
  return body;
}

function App() {
  const [products, setProducts] = useState<Product[]>([]);
  const [selected, setSelected] = useState<Product | null>(null);
  const [form, setForm] = useState<ProductForm>(emptyForm);
  const [keyword, setKeyword] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  async function loadProducts(searchTerm = "") {
    setLoading(true);
    setMessage("");
    const path = searchTerm.trim()
      ? `/api/products/search?keyword=${encodeURIComponent(searchTerm.trim())}`
      : "/api/products";
    try {
      const items = await parseResponse<Product[]>(await fetch(`${API_BASE}${path}`));
      setProducts(items);
      if (items.length === 0) {
        setSelected(null);
      }
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Không thể tải danh sách sản phẩm");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadProducts();
  }, []);

  function updateField<K extends keyof ProductForm>(key: K, value: ProductForm[K]) {
    setForm((current) => ({ ...current, [key]: value }));
  }

  function startCreate() {
    setSelected(null);
    setForm(emptyForm);
    setMessage("");
  }

  function startEdit(product: Product) {
    setSelected(product);
    setForm(toForm(product));
    setMessage("");
  }

  async function saveProduct(event: FormEvent) {
    event.preventDefault();
    setLoading(true);
    setMessage("");
    const minimumStock = form.minimumStock === "" ? null : Number(form.minimumStock);
    const body = {
      product_code: form.productCode,
      product_name: form.productName,
      description: form.description,
      unit: form.unit,
      quantity: Number(form.quantity),
      minimum_stock: minimumStock
    };

    try {
      if (selected) {
        const updated = await parseResponse<Product>(
          await fetch(`${API_BASE}/api/products/${selected.id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              product_name: body.product_name,
              description: body.description,
              unit: body.unit,
              minimum_stock: body.minimum_stock
            })
          })
        );
        if (updated.quantity !== body.quantity) {
          await parseResponse<Product>(
            await fetch(`${API_BASE}/api/products/${selected.id}/quantity`, {
              method: "PATCH",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ quantity: body.quantity })
            })
          );
        }
        setMessage("Cập nhật sản phẩm thành công");
      } else {
        await parseResponse<Product>(
          await fetch(`${API_BASE}/api/products`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body)
          })
        );
        setMessage("Tạo sản phẩm thành công");
      }
      startCreate();
      await loadProducts(keyword);
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Không thể lưu sản phẩm");
    } finally {
      setLoading(false);
    }
  }

  async function deleteProduct(product: Product) {
    const confirmed = window.confirm(`Xoá sản phẩm ${product.productCode}?`);
    if (!confirmed) return;
    setLoading(true);
    try {
      await parseResponse<{ deleted: boolean }>(
        await fetch(`${API_BASE}/api/products/${product.id}`, { method: "DELETE" })
      );
      setMessage("Xoá sản phẩm thành công");
      if (selected?.id === product.id) startCreate();
      await loadProducts(keyword);
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Không thể xoá sản phẩm");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="page">
      <section className="hero">
        <p className="eyebrow">Inventory Operations</p>
        <h1>Quản lý kho</h1>
        <p>Tạo, tìm kiếm, cập nhật và kiểm soát trạng thái tồn kho trong một màn hình gọn.</p>
      </section>

      <section className="toolbar">
        <input
          value={keyword}
          onChange={(event) => setKeyword(event.target.value)}
          placeholder="Nhập mã hoặc tên sản phẩm"
        />
        <button onClick={() => loadProducts(keyword)} disabled={loading}>Tìm kiếm</button>
        <button onClick={() => { setKeyword(""); void loadProducts(); }} disabled={loading}>Tải lại</button>
        <button onClick={startCreate}>Tạo sản phẩm</button>
      </section>

      {message && <p className="message">{message}</p>}

      <section className="content">
        <div className="card table-card">
          <h2>Danh sách sản phẩm</h2>
          {products.length === 0 ? (
            <p className="empty">{keyword ? "Không tìm thấy sản phẩm phù hợp" : "Chưa có sản phẩm trong kho"}</p>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Mã</th>
                  <th>Tên sản phẩm</th>
                  <th>Đơn vị</th>
                  <th>Số lượng</th>
                  <th>Trạng thái</th>
                  <th>Hành động</th>
                </tr>
              </thead>
              <tbody>
                {products.map((product) => (
                  <tr key={product.id}>
                    <td>{product.productCode}</td>
                    <td>{product.productName}</td>
                    <td>{product.unit}</td>
                    <td>{product.quantity}</td>
                    <td><span className={`badge ${product.status.toLowerCase()}`}>{product.status}</span></td>
                    <td className="actions">
                      <button onClick={() => startEdit(product)}>Xem/Sửa</button>
                      <button className="danger" onClick={() => deleteProduct(product)}>Xoá</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        <form className="card form-card" onSubmit={saveProduct}>
          <h2>{selected ? "Chi tiết / Cập nhật sản phẩm" : "Tạo sản phẩm"}</h2>
          <label>Mã sản phẩm
            <input value={form.productCode} disabled={Boolean(selected)} required maxLength={50} onChange={(event) => updateField("productCode", event.target.value)} />
          </label>
          <label>Tên sản phẩm
            <input value={form.productName} required maxLength={255} onChange={(event) => updateField("productName", event.target.value)} />
          </label>
          <label>Mô tả
            <textarea value={form.description} maxLength={1000} onChange={(event) => updateField("description", event.target.value)} />
          </label>
          <div className="grid">
            <label>Đơn vị
              <input value={form.unit} required onChange={(event) => updateField("unit", event.target.value)} />
            </label>
            <label>Số lượng
              <input type="number" min="0" value={form.quantity} required onChange={(event) => updateField("quantity", Number(event.target.value))} />
            </label>
          </div>
          <label>Tồn kho tối thiểu
            <input type="number" min="0" value={form.minimumStock} onChange={(event) => updateField("minimumStock", event.target.value)} />
          </label>
          {selected && (
            <div className="detail">
              <span>Trạng thái hiện tại: <strong>{selected.status}</strong></span>
              <span>Cập nhật lần cuối: {selected.updatedAt}</span>
            </div>
          )}
          <div className="actions">
            <button type="submit" disabled={loading}>Lưu</button>
            <button type="button" onClick={startCreate}>Huỷ</button>
          </div>
        </form>
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")!).render(<App />);
