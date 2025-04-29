<template>
  <div class="container mx-auto p-4">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">产品管理</h1>
      <Link href="/products/create" class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded">
      添加产品
      </Link>
    </div>

    <!-- 搜索栏 -->
    <div class="mb-6">
      <form @submit.prevent="search">
        <div class="flex">
          <input v-model="searchQuery" type="text" placeholder="搜索产品名称..."
            class="border border-gray-300 rounded-l px-4 py-2 w-full" />
          <button type="submit" class="bg-gray-200 hover:bg-gray-300 px-4 py-2 rounded-r">
            搜索
          </button>
        </div>
      </form>
    </div>

    <!-- 产品列表 -->
    <div class="overflow-x-auto bg-white rounded-lg shadow">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              ID
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              产品名称
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              价格
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              库存状态
            </th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
              操作
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="product in products" :key="product.id">
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ product.id }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
              {{ product.name }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              ¥{{ product.price.toFixed(2) }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span :class="[
                'px-2 inline-flex text-xs leading-5 font-semibold rounded-full',
                product.in_stock
                  ? 'bg-green-100 text-green-800'
                  : 'bg-red-100 text-red-800',
              ]">
                {{ product.in_stock ? '有库存' : '无库存' }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
              <div class="flex justify-end space-x-2">
                <Link :href="`/products/${product.id}`" class="text-indigo-600 hover:text-indigo-900">
                查看
                </Link>
                <Link :href="`/products/${product.id}/edit`" class="text-blue-600 hover:text-blue-900">
                编辑
                </Link>
                <button @click="confirmDelete(product)" class="text-red-600 hover:text-red-900">
                  删除
                </button>
              </div>
            </td>
          </tr>

          <!-- 无数据提示 -->
          <tr v-if="products.length === 0">
            <td colspan="5" class="px-6 py-4 text-center text-gray-500">
              暂无产品数据
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 分页 -->
    <div class="mt-4 flex justify-between items-center">
      <div class="text-sm text-gray-700">
        共 <span class="font-medium">{{ pagination.total }}</span> 条记录
      </div>
      <div class="flex space-x-1">
        <button v-for="pageNumber in totalPages" :key="pageNumber" @click="goToPage(pageNumber)"
          :disabled="pageNumber === pagination.page" :class="[
            'px-3 py-1 border rounded',
            pageNumber === pagination.page
              ? 'bg-blue-500 text-white'
              : 'bg-white text-gray-700 hover:bg-gray-50',
          ]">
          {{ pageNumber }}
        </button>
      </div>
    </div>

    <!-- 删除确认对话框 -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white p-6 rounded-lg shadow-lg w-full max-w-md">
        <h3 class="text-lg font-bold mb-4">确认删除</h3>
        <p class="mb-6">您确定要删除产品"{{ productToDelete?.name }}"吗？此操作不可恢复。</p>
        <div class="flex justify-end space-x-3">
          <button @click="showDeleteModal = false" class="px-4 py-2 border border-gray-300 rounded hover:bg-gray-100">
            取消
          </button>
          <button @click="deleteProduct" class="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600">
            确认删除
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { router, Link } from '@inertiajs/vue3';

// 从属性中获取产品列表和分页信息
const props = defineProps({
  products: Array,
  pagination: Object,
  search: String
});

// 搜索功能
const searchQuery = ref(props.search);

function search() {
  router.get('/products', {
    search: searchQuery.value,
    page: 1 // 重置到第一页
  }, {
    preserveState: true,
    replace: true
  });
}

// 分页功能
const totalPages = computed(() => {
  return Math.ceil(props.pagination.total / props.pagination.per_page);
});

function goToPage(page) {
  router.get('/products', {
    search: searchQuery.value,
    page: page
  }, {
    preserveState: true,
    replace: true
  });
}

// 删除功能
const showDeleteModal = ref(false);
const productToDelete = ref(null);

function confirmDelete(product) {
  productToDelete.value = product;
  showDeleteModal.value = true;
}

function deleteProduct() {
  if (!productToDelete.value) return;

  router.delete(`/products/${productToDelete.value.id}`, {}, {
    onSuccess: () => {
      showDeleteModal.value = false;
      productToDelete.value = null;
    }
  });
}
</script>