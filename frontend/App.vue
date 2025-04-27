<script setup>
import { ref } from 'vue';
import ProductList from '@/components/ProductList.vue';

// 主页导航状态
const currentPage = ref('products');
</script>

<template>
  <div class="app-container">
    <header class="bg-gray-800 text-white p-4">
      <div class="container mx-auto flex justify-between items-center">
        <h1 class="text-xl font-bold">产品管理系统</h1>
        <nav>
          <ul class="flex space-x-4">
            <li>
              <a @click="currentPage = 'products'" 
                 class="cursor-pointer hover:text-blue-300"
                 :class="{ 'text-blue-300': currentPage === 'products' }">
                产品管理
              </a>
            </li>
            <!-- 可以在此处添加更多导航链接 -->
          </ul>
        </nav>
      </div>
    </header>
    
    <main class="container mx-auto mt-6">
      <!-- 根据当前页面状态显示不同组件 -->
      <ProductList v-if="currentPage === 'products'" />
    </main>
    
    <footer class="mt-12 py-4 bg-gray-100">
      <div class="container mx-auto text-center text-gray-500">
        <p>产品管理系统 &copy; {{ new Date().getFullYear() }}</p>
      </div>
    </footer>
  </div>
</template>

<style>
/* 全局样式 */
body {
  font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
  line-height: 1.5;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

main {
  flex: 1;
}
</style>
