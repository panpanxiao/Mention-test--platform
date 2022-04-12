'use strict'
const path = require('path')
const defaultSettings = require('./src/settings.js')

function resolve(dir) {
  return path.join(__dirname, dir)
}

const name = defaultSettings.title || 'vue Admin Template' // page title

const port = process.env.port || process.env.npm_config_port || 9528 // dev port

module.exports = {
  publicPath: './',                                     // 基本路径
  outputDir: process.env.outputDir,                     // 配置文件中的值，用于修改打包文件名称
  lintOnSave: false,                                    // eslint-loader 是否在保存的时候检查
  assetsDir: 'static',                                  // 输出的资源，所在的文件夹
  productionSourceMap: false,                           // 如果你不需要生产环境的 source map，可以将其设置为 false 以加速生产环境构建
  filenameHashing: false,                               // build之后生成的静态资源默认情况下加了hash值以控制静态资源的缓存，默认是true
  devServer: {
    https: false,                                       // https: { type: Boolean }
    port: port,                                         // 端口号
    open: true,                                         // 配置自动启动浏览器 true/false
    overlay: {
      warnings: false,
      errors: true
    },
    proxy: {
      '/api': {
        target: 'http://10.241.152.129:8081',               // 要访问的跨域的域名
        changeOrigin: true,                             // 开启代理：在本地会创建一个虚拟服务端，然后发送请求的数据，并同时接收请求的数据，这样客户端和服务端进行数据的交互就不会有跨域问题
        secure: false,                                  // 使用的是http协议则设置为false，https协议则设置为true
        ws: true,                                       // 是否启用websockets
        pathRewrite: {
          '^/api': ''
        }
      }
    }
  },
  // webpack配置 https://github.com/vuejs/vue-cli/blob/dev/docs/webpack.md
  configureWebpack: {
    name: name,
    resolve: {
      alias: {
        '@': resolve('src')
      }
    }
  },
  chainWebpack(config) {
    config.plugin('preload').tap(() => [
      {
        rel: 'preload',
        fileBlacklist: [/\.map$/, /hot-update\.js$/, /runtime\..*\.js$/],
        include: 'initial'
      }
    ])
    config.plugins.delete('prefetch')
    config.module
      .rule('svg')
      .exclude.add(resolve('src/icons'))
      .end()
    config.module
      .rule('icons')
      .test(/\.svg$/)
      .include.add(resolve('src/icons'))
      .end()
      .use('svg-sprite-loader')
      .loader('svg-sprite-loader')
      .options({
        symbolId: 'icon-[name]'
      })
      .end()
    config
      .when(process.env.NODE_ENV !== 'development',
        config => {
          config
            .plugin('ScriptExtHtmlWebpackPlugin')
            .after('html')
            .use('script-ext-html-webpack-plugin', [{
              inline: /runtime\..*\.js$/
            }])
            .end()
          config
            .optimization.splitChunks({
              chunks: 'all',
              cacheGroups: {
                libs: {
                  name: 'chunk-libs',
                  test: /[\\/]node_modules[\\/]/,
                  priority: 10,
                  chunks: 'initial'
                },
                elementUI: {
                  name: 'chunk-elementUI',
                  priority: 20,
                  test: /[\\/]node_modules[\\/]_?element-ui(.*)/
                },
                commons: {
                  name: 'chunk-commons',
                  test: resolve('src/components'),
                  minChunks: 3,
                  priority: 5,
                  reuseExistingChunk: true
                }
              }
            })
          // https:// webpack.js.org/configuration/optimization/#optimizationruntimechunk
          config.optimization.runtimeChunk('single')
        }
      )
  }
}
