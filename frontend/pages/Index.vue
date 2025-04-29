<template>
  <div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-6">欢迎使用产品管理系统</h1>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div class="bg-white p-6 rounded-lg shadow-md">
        <h2 class="text-xl font-semibold mb-3">产品管理</h2>
        <p class="text-gray-600 mb-4">
          管理您的产品信息，包括名称、价格、描述和库存状态。
        </p>
        <Link href="/products" class="inline-block bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded">
        进入产品管理
        </Link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { router, Link } from '@inertiajs/vue3';

defineProps({
  name: String
});
</script>