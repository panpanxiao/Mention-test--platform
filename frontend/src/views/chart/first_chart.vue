<template>
  <div class="app-container">
    <div ref="pieChartDemo" style="width: 500px;height: 500px;" />
  </div>

</template>

<script>
import * as echarts from 'echarts'

export default {
  name: 'EchartDemo',
  mounted() {
    this.initPieChart()
  },

  methods: {
    initPieChart() {
      var chartDom = this.$refs['pieChartDemo']
      var myChart = echarts.init(chartDom)
      var option = {
        title: {
          text: 'MiTV Test',
          subtext: '测试类型分布',
          left: 'center'
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'left'
        },
        series: [
          {
            name: 'Access From',
            type: 'pie',
            radius: '50%',
            data: [
              { value: 20, name: 'Special testing' },
              { value: 2, name: 'Performance testing' },
              { value: 1, name: 'Security testing' },
              { value: 3, name: 'Function testing' },
              { value: 5, name: 'Compatibility testing' }
            ]
          }
        ]
      }
      option && myChart.setOption(option)
    }
  }
}
</script>
