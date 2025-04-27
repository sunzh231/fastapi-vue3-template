// API服务封装
import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 产品相关API
export const productApi = {
  // 获取所有产品
  getProducts() {
    return api.get('/products');
  },
  
  // 获取单个产品
  getProduct(id) {
    return api.get(`/products/${id}`);
  },
  
  // 创建产品
  createProduct(data) {
    return api.post('/products', data);
  },
  
  // 更新产品
  updateProduct(id, data) {
    return api.put(`/products/${id}`, data);
  },
  
  // 删除产品
  deleteProduct(id) {
    return api.delete(`/products/${id}`);
  }
};

export default api;
