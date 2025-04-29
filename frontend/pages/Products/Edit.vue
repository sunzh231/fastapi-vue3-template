<template>
  <div class="container mx-auto p-4">
    <div class="mb-6">
      <Link href="/products" class="text-blue-500 hover:text-blue-700">
      &larr; 返回产品列表
      </Link>
    </div>

    <div class="bg-white shadow rounded-lg p-6">
      <h1 class="text-2xl font-bold mb-6">编辑产品</h1>

      <form @submit.prevent="submit">
        <div class="mb-4">
          <label for="name" class="block text-sm font-medium text-gray-700 mb-1">产品名称</label>
          <input id="name" v-model="form.name" type="text"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :class="{ 'border-red-500': errors.name }" required />
          <p v-if="errors.name" class="mt-1 text-sm text-red-600">{{ errors.name }}</p>
        </div>

        <div class="mb-4">
          <label for="price" class="block text-sm font-medium text-gray-700 mb-1">价格</label>
          <input id="price" v-model="form.price" type="number" step="0.01" min="0"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :class="{ 'border-red-500': errors.price }" required />
          <p v-if="errors.price" class="mt-1 text-sm text-red-600">{{ errors.price }}</p>
        </div>

        <div class="mb-4">
          <label for="description" class="block text-sm font-medium text-gray-700 mb-1">产品描述</label>
          <textarea id="description" v-model="form.description" rows="4"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :class="{ 'border-red-500': errors.description }"></textarea>
          <p v-if="errors.description" class="mt-1 text-sm text-red-600">{{ errors.description }}</p>
        </div>

        <div class="mb-6">
          <label class="inline-flex items-center">
            <input type="checkbox" v-model="form.in_stock"
              class="rounded border-gray-300 text-blue-600 focus:ring-blue-500" />
            <span class="ml-2 text-sm text-gray-700">有库存</span>
          </label>
        </div>

        <div class="flex justify-end">
          <button type="submit" class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded flex items-center"
            :disabled="processing">
            <span v-if="processing" class="mr-2">
              正在保存...
            </span>
            <span v-else>
              保存更改
            </span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue';
import { router, Link } from '@inertiajs/vue3';

// 从属性中获取产品数据
const props = defineProps({
  product: Object
});

// 表单数据，使用产品数据初始化
const form = reactive({
  name: props.product.name,
  price: props.product.price,
  description: props.product.description || '',
  in_stock: props.product.in_stock
});

// 错误信息
const errors = reactive({});

// 处理状态
const processing = ref(false);

// 表单提交
function submit() {
  processing.value = true;

  // 清空错误
  Object.keys(errors).forEach(key => delete errors[key]);

  // 表单验证
  let hasError = false;

  if (!form.name) {
    errors.name = '产品名称不能为空';
    hasError = true;
  }

  if (!form.price) {
    errors.price = '价格不能为空';
    hasError = true;
  } else if (isNaN(parseFloat(form.price)) || parseFloat(form.price) < 0) {
    errors.price = '价格必须是非负数';
    hasError = true;
  }

  if (hasError) {
    processing.value = false;
    return;
  }

  // 提交表单
  router.put(`/products/${props.product.id}`, form, {
    onError: (errors) => {
      // 设置错误信息
      Object.assign(errors, errors);
      processing.value = false;
    },
    onSuccess: () => {
      processing.value = false;
    }
  });
}
</script>