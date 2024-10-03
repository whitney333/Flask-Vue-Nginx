const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  publicPath: '',
  transpileDependencies: true,
  configureWebpack: {
    devServer: {
      proxy: {
        '/api': {
          target: 'http://127.0.0.1:5000/',
          changeOrigin: true,
          pathRewrite: {
            '^/api': '/'
          }
        }
      }
    }
  }
})
