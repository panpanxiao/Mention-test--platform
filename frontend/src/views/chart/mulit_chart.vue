<template>
  <div class="projectCost">
    <div class="container">
      <div v-for="(item,index) in list" :key="index" class="wrapper">
        <div class="roseChart" />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      list: [
        {
          id: 1,
          price: {
            name: '项目一',
            resData: [
              {
                name: '订购费用',
                value: 12
              },
              {
                name: '饲养费用',
                value: 18
              },
              {
                name: '实验费用',
                value: 8
              },
              {
                name: '其他费用',
                value: 10
              }
            ]
          }
        },
        {
          id: 2,
          price: {
            name: '项目二',
            resData: [
              {
                name: '订购费用',
                value: 18
              },
              {
                name: '饲养费用',
                value: 10
              },
              {
                name: '实验费用',
                value: 20
              },
              {
                name: '其他费用',
                value: 9
              }
            ]
          }
        }
      ]
    }
  },
  mounted() {
    this.drawRose()
  },
  methods: {
    drawRose() {
      var echarts = require('echarts')
      var roseCharts = document.getElementsByClassName('roseChart') // 对应地使用ByClassName
      for (var i = 0; i < roseCharts.length; i++) { // 通过for循环，在相同class的dom内绘制元素
        var myChart = echarts.init(roseCharts[i])
        myChart.setOption({
          color: ['#4DFFFD', '#7B3FF6', '#1F6DFE', '#34A6FE'],
          title: {
            text: this.list[i].price.name,
            left: '70',
            top: 5,
            textStyle: {
              color: '#4DFFFD',
              fontSize: 14
            }
          },
          tooltip: {
            trigger: 'item',
            formatter: '{b} : {c} ({d}%)'
          },
          legend: {
            type: 'scroll',
            orient: 'vartical',
            top: 'center',
            right: '0px',
            itemWidth: 16,
            itemHeight: 8,
            itemGap: 16,
            textStyle: {
              color: '#FFFFFF',
              fontSize: 12
            },
            data: ['订购费用', '饲养费用', '实验费用', '其他费用']
          },
          polar: {
            center: ['36%', '56%']
          },
          angleAxis: {
            interval: 3, // 强制设置坐标轴分割间隔
            type: 'category',
            z: 10,
            axisLine: {
              show: false
            },
            axisLabel: {
              show: false
            }
          },
          radiusAxis: {
            min: 10,
            max: 1000,
            interval: 200,
            axisLine: {
              show: false
            },
            axisLabel: {
              show: false
            },
            splitLine: {
              lineStyle: {
                color: '#2277C3',
                width: 1,
                type: 'solid'
              }
            }
          },
          calculable: true,
          series: [
            {
              type: 'pie',
              radius: ['10%', '14%'],
              center: ['36%', '56%'],
              hoverAnimation: false,
              labelLine: {
                show: false
              },
              data: [{
                value: 0,
                itemStyle: {
                  normal: {
                    color: '#809DF5'
                  }
                }
              }]
            },
            {
              stack: 'a',
              type: 'pie',
              radius: ['20%', '80%'],
              center: ['36%', '56%'],
              roseType: 'area',
              zlevel: 10,
              label: {
                show: false
              },
              labelLine: {
                show: false
              },
              data: this.list[i].price.resData // 渲染每个图表对应的数据
            }]
        })
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.projectCost{
  margin-left: 40px;
  .container{
    display: flex;
    width: 680px;
    height: 240px;
    background-size: 100% 100%;
    // background-image: url('../../../assets/images/projectTest/costDetail.png');
    .wrapper{
      margin-top: 20px;
      width: 340px;
      height:180px;
      border-right: 1px solid #0B61B3;
      .roseChart{
        width: 260px;
        height:180px;
      }
    }
  }
}
</style>

