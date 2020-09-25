<template>
  <div id="app">
      <iframe
         style="border:none"
         :width="searchTableWidth"
         :height="searchTableHeight"
         v-bind:src="reportUrl"
       ></iframe>
  </div>
</template>
<script>
import Vue from 'vue'
export default {
  methods: {
    widthHeight() {
      this.searchTableHeight = window.innerHeight -146;
      this.searchTableWidth = window.innerWidth - 280
    },
  },
  data() {
    return {
      reportUrl: '',
      searchTableHeight: 0,
      searchTableWidth: 0
    }
  },
   mounted() {
    window.onresize = () => {
      this.widthHeight(); // 自适应高宽度
    };
    this.$nextTick(function () {
      this.widthHeight();
    });
  },
  created() {
    // 从路由里动态获取 url地址
    this.reportUrl= this.$route.query.locust_url;
 
    
   
    

 

  },
}
</script>