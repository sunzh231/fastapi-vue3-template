<template>
  <div class="container mx-auto p-4">
    <div class="mb-6">
      <Link href="/products" class="text-blue-500 hover:text-blue-700">
      &larr; 返回产品列表
      </Link>
    </div>

    <div class="bg-white shadow rounded-lg p-6">
      <div class="flex justify-between items-start mb-6">
        <h1 class="text-2xl font-bold">{{ product.name }}</h1>
        <div class="flex space-x-2">
          <Link :href="`/products/${product.id}/edit`"
            class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded">
          编辑
          </Link>
          <button @click="confirmDelete" class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded">
            删除
          </button>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <div class="mb-4">
            <h2 class="text-sm font-medium text-gray-500">产品ID</h2>
            <p class="text-lg">{{ product.id }}</p>
          </div>

          <div class="mb-4">
            <h2 class="text-sm font-medium text-gray-500">价格</h2>
            <p class="text-lg">¥{{ product.price.toFixed(2) }}</p>
          </div>

          <div class="mb-4">
            <h2 class="text-sm font-medium text-gray-500">库存状态</h2>
            <p>
              <span :class="[
                'px-2 py-1 text-sm font-semibold rounded-full',
                product.in_stock
                  ? 'bg-green-100 text-green-800'
                  : 'bg-red-100 text-red-800',
              ]">
                {{ product.in_stock ? '有库存' : '无库存' }}
              </span>
            </p>
          </div>
        </div>

        <div>
          <div class="mb-4">
            <h2 class="text-sm font-medium text-gray-500">创建时间</h2>
            <p class="text-lg">{{ formatDate(product.created_at) }}</p>
          </div>

          <div class="mb-4">
            <h2 class="text-sm font-medium text-gray-500">更新时间</h2>
            <p class="text-lg">{{ formatDate(product.updated_at) }}</p>
          </div>
        </div>
      </div>

      <div class="mt-6">
        <h2 class="text-sm font-medium text-gray-500 mb-2">产品描述</h2>
        <p class="text-gray-700">{{ product.description || '暂无描述' }}</p>
      </div>
    </div>

    <!-- 删除确认对话框 -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white p-6 rounded-lg shadow-lg w-full max-w-md">
        <h3 class="text-lg font-bold mb-4">确认删除</h3>
        <p class="mb-6">您确定要删除产品"{{ product.name }}"吗？此操作不可恢复。</p>
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
import { ref } from 'vue';
import { router, Link } from '@inertiajs/vue3';

const props = defineProps({
  product: Object
});

// 删除功能
const showDeleteModal = ref(false);

function confirmDelete() {
  showDeleteModal.value = true;
}

function deleteProduct() {
  router.delete(`/products/${props.product.id}`, {}, {
    onSuccess: () => {
      showDeleteModal.value = false;
    }
  });
}

// 日期格式化
function formatDate(dateString) {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  });
}
</script>