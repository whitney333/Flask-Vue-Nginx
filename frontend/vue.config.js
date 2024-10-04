const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  publicPath: '',
  transpileDependencies: true,
  // needed when dev in local
  // configureWebpack: {
  //   devServer: {
  //     proxy: {
  //       '/api': {
  //         target: 'http://127.0.0.1:5000/',
  //         changeOrigin: true,
  //         pathRewrite: {
  //           '^/api': '/'
  //         }
  //       }
  //     }
  //   }
  // }
})
