<script setup>
import { ref, onMounted } from 'vue';
import { productApi } from '../services/api';

// 产品列表状态
const products = ref([]);
const loading = ref(false);
const error = ref(null);

// 表单状态
const formData = ref({
  id: null,
  name: '',
  description: '',
  price: 0,
  in_stock: true
});
const showForm = ref(false);
const editMode = ref(false);

// 加载产品数据
const fetchProducts = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    const response = await productApi.getProducts();
    products.value = response.data;
  } catch (err) {
    error.value = '加载产品数据失败: ' + (err.response?.data?.detail || err.message);
    console.error('加载产品数据失败:', err);
  } finally {
    loading.value = false;
  }
};

// 打开创建表单
const openCreateForm = () => {
  formData.value = {
    id: null,
    name: '',
    description: '',
    price: 0,
    in_stock: true
  };
  editMode.value = false;
  showForm.value = true;
};

// 打开编辑表单
const openEditForm = (product) => {
  formData.value = { ...product };
  editMode.value = true;
  showForm.value = true;
};

// u5173u95edu8868u5355
const closeForm = () => {
  showForm.value = false;
};

// 保存表单
const saveProduct = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    if (editMode.value) {
      // 编辑模式
      await productApi.updateProduct(formData.value.id, formData.value);
    } else {
      // 创建模式
      await productApi.createProduct(formData.value);
    }
    
    // 刷新产品列表
    await fetchProducts();
    // 关闭表单
    showForm.value = false;
  } catch (err) {
    error.value = '保存产品失败: ' + (err.response?.data?.detail || err.message);
    console.error('保存产品失败:', err);
  } finally {
    loading.value = false;
  }
};

// 删除产品
const deleteProduct = async (id) => {
  if (!confirm('确定要删除此产品吗？')) return;
  
  loading.value = true;
  error.value = null;
  
  try {
    await productApi.deleteProduct(id);
    // 刷新产品列表
    await fetchProducts();
  } catch (err) {
    error.value = '删除产品失败: ' + (err.response?.data?.detail || err.message);
    console.error('删除产品失败:', err);
  } finally {
    loading.value = false;
  }
};

// 页面加载时获取产品数据
onMounted(() => {
  fetchProducts();
});
</script>

<template>
  <div class="products-container p-4">
    <div class="header flex justify-between items-center mb-4">
      <h1 class="text-2xl font-bold">产品管理</h1>
      <button @click="openCreateForm" class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
        新增产品
      </button>
    </div>
    
    <!-- 错误提示 -->
    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      {{ error }}
    </div>
    
    <!-- 加载状态 -->
    <div v-if="loading" class="text-center py-4">
      <div class="loader"></div>
      <p>加载中...</p>
    </div>
    
    <!-- 产品列表 -->
    <div v-else-if="products.length" class="grid gap-4">
      <table class="min-w-full bg-white border border-gray-200">
        <thead>
          <tr>
            <th class="py-2 px-4 border-b border-gray-200 bg-gray-50 text-left">ID</th>
            <th class="py-2 px-4 border-b border-gray-200 bg-gray-50 text-left">名称</th>
            <th class="py-2 px-4 border-b border-gray-200 bg-gray-50 text-left">描述</th>
            <th class="py-2 px-4 border-b border-gray-200 bg-gray-50 text-left">价格</th>
            <th class="py-2 px-4 border-b border-gray-200 bg-gray-50 text-left">库存状态</th>
            <th class="py-2 px-4 border-b border-gray-200 bg-gray-50 text-left">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in products" :key="product.id" class="hover:bg-gray-50">
            <td class="py-2 px-4 border-b border-gray-200">{{ product.id }}</td>
            <td class="py-2 px-4 border-b border-gray-200">{{ product.name }}</td>
            <td class="py-2 px-4 border-b border-gray-200">{{ product.description || '-' }}</td>
            <td class="py-2 px-4 border-b border-gray-200">{{ product.price.toFixed(2) }}</td>
            <td class="py-2 px-4 border-b border-gray-200">{{ product.in_stock ? '有货' : '缺货' }}</td>
            <td class="py-2 px-4 border-b border-gray-200">
              <div class="flex space-x-2">
                <button @click="openEditForm(product)" 
                  class="px-3 py-1 bg-yellow-500 text-white rounded hover:bg-yellow-600">
                  编辑
                </button>
                <button @click="deleteProduct(product.id)" 
                  class="px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600">
                  删除
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <!-- 空状态 -->
    <div v-else class="text-center py-8 bg-gray-50 rounded">
      <p class="text-gray-500">暂无产品数据</p>
    </div>
    
    <!-- 产品表单 -->
    <div v-if="showForm" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
      <div class="bg-white rounded-lg shadow-lg p-6 w-full max-w-md">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-bold">{{ editMode ? '编辑产品' : '新增产品' }}</h2>
          <button @click="closeForm" class="text-gray-500 hover:text-gray-700">×</button>
        </div>
        
        <form @submit.prevent="saveProduct" class="space-y-4">
          <!-- 产品名称 -->
          <div>
            <label class="block text-sm font-medium text-gray-700">产品名称</label>
            <input v-model="formData.name" type="text" required
              class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3">
          </div>
          
          <!-- 产品描述 -->
          <div>
            <label class="block text-sm font-medium text-gray-700">产品描述</label>
            <textarea v-model="formData.description"
              class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3" rows="3"></textarea>
          </div>
          
          <!-- 产品价格 -->
          <div>
            <label class="block text-sm font-medium text-gray-700">产品价格</label>
            <input v-model.number="formData.price" type="number" min="0" step="0.01" required
              class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3">
          </div>
          
          <!-- 库存状态 -->
          <div>
            <label class="block text-sm font-medium text-gray-700">库存状态</label>
            <select v-model="formData.in_stock" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3">
              <option :value="true">有货</option>
              <option :value="false">缺货</option>
            </select>
          </div>
          
          <!-- 提交按钮 -->
          <div class="flex justify-end space-x-2">
            <button type="button" @click="closeForm" 
              class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50">
              取消
            </button>
            <button type="submit"
              class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-500 hover:bg-blue-600">
              保存
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.loader {
  border: 3px solid #f3f3f3;
  border-radius: 50%;
  border-top: 3px solid #3498db;
  width: 24px;
  height: 24px;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
