<script>
import * as echarts from 'echarts';

export default {
  data() {
    return {
      barWidthNumber: 69,
      axisLabelFontSize: 14,
      axisNameFontSize: 16,
      chart: null,
      chartOptions: {
        title: {
          text: 'Feature Importance',
          left: 'center',
          textStyle: {
            fontSize: 18,
          },
        },
        xAxis: {
          name: 'Feature Importance',
          axisLabel: {
            fontSize: 14,
          },
          nameTextStyle: {
            fontSize: 16,
          },
        },
        yAxis: {
          name: 'Features',
          axisLabel: {
            fontSize: 14,
          },
          nameTextStyle: {
            fontSize: 16,
          },
        },
        series: {
          label: {
            show: true,
            position: 'right',
          },
          itemStyle: {
            color: '#5470c6',
          },
          barWidth: "69%",
        },
      }
    };
  },
  mounted() {
    // dispose chart if it exists
    if (this.chartInstance) {
      this.chart.dispose();
    }
    // add listener to window resize
    window.addEventListener('resize', () => {
      // resize feature importance div
      // make it 7:5
      let chartContainer = document.getElementById('feature-importance');
      let chartContainerWidth = chartContainer.clientWidth;
      let chartContainerHeight = chartContainer.clientWidth
      // resize chart
      this.chart.resize();
    });
  },
  name: 'Right',
  props: {
    importances: Object,
    chartInstance: Object
  },
  watch: {
    importances: {
      handler: function (val) {
        this.drawChart(val);
      },
      deep: true
    },
    chartOptions: {
      handler: function (val) {
        this.chart.setOption(val);
      },
      deep: true
    },
    barWidthNumber: {
      handler: function (val) {
        this.chartOptions.series.barWidth = val + '%';
        this.chart.setOption(this.chartOptions);
      }
    },
    axisLabelFontSize: {
      handler: function (val) {
        this.chartOptions.xAxis.axisLabel.fontSize = val;
        this.chartOptions.yAxis.axisLabel.fontSize = val;
        this.chart.setOption(this.chartOptions);
      }
    },
    axisNameFontSize: {
      handler: function (val) {
        this.chartOptions.xAxis.nameTextStyle.fontSize = val;
        this.chartOptions.yAxis.nameTextStyle.fontSize = val;
        this.chart.setOption(this.chartOptions);
      }
    }
  },

  methods: {


    drawChart(importances) {
      if (this.chart) {
        this.chart.dispose();
      }
      this.chart = echarts.init(document.getElementById('feature-importance'));
      let option = {
        title: {
          text: 'Feature Importance',
          left: 'center',
          top: 20,
        },
        toolbox: {
          feature: {
            saveAsImage: { show: true, title: 'Save', pixelRatio: 2 }
          }
        },
        tooltip: {
          trigger: 'axis',

          axisPointer: {
            type: 'shadow',
          }
        },
        grid: {
          left: '6%',
          right: '6%',
          bottom: '10%',
          containLabel: true,
          show: true
        },
        xAxis: {
          name: 'Feature Importance',
          nameLocation: 'center',
          nameGap: 30,
          nameTextStyle: {
            fontSize: 16
          },
          axisLabel: {
            fontSize: 14,
          },
          type: 'value',
          boundaryGap: [0, 0.01]
        },
        yAxis: {
          name: 'Features',
          nameLocation: 'center',
          nameGap: 30,
          nameTextStyle: {
            fontSize: 16
          },
          axisLabel: {
            fontSize: 14,
          },
          type: 'category',
          data: Object.keys(importances)
        },
        series: [
          {
            name: 'Feature Importance',
            type: 'bar',
            data: Object.values(importances),
            label: {
              show: true,
              position: 'right',
            },
          }
        ],
      };
      this.chart.setOption(option);
      this.chart.setOption(this.chartOptions);
    }
  },
}
</script>


<template>
  <div class="right-show">
    <div id="feature-importance" class="right-show-chart"></div>
  </div>
  <div class="chart-options">
    <h2>图表调整</h2>
    <div class="options">
      <div class="chart-option">
        <label for="title-text">标题</label>
        <textarea v-model="chartOptions.title.text"></textarea>
      </div>
      <div class="chart-option">
        <label for="text-size">标题字体大小</label>
        <input type="range" v-model="chartOptions.title.textStyle.fontSize" max="28" min="12">
        {{ chartOptions.title.textStyle.fontSize }}
      </div>
      <div class="chart-option">
        <label for="text-size">X 轴名称</label>
        <textarea v-model="chartOptions.xAxis.name"></textarea>
      </div>
      <div class="chart-option">
        <label for="text-size">Y 轴名称</label>
        <textarea v-model="chartOptions.yAxis.name"></textarea>
      </div>
      <div class="chart-option">
        <label for="text-size">轴刻度字体大小</label>
        <input type="range" v-model="axisLabelFontSize" max="20" min="10">{{ chartOptions.xAxis.axisLabel.fontSize }}
      </div>
      <div class="chart-option">
        <label for="text-size">轴名称字体大小</label>
        <input type="range" v-model="axisNameFontSize" max="20" min="10">
        {{ chartOptions.xAxis.nameTextStyle.fontSize }}
      </div>
      <div class="chart-option">
        <label for="bar-width">柱状图宽度</label>
        <input type="range" v-model="barWidthNumber" max="100" min="10">
        {{ chartOptions.series.barWidth }}
      </div>
      <div class="chart-option">
        <label for="item-color">柱状图颜色</label>
        <input type="color" v-model="chartOptions.series.itemStyle.color">
      </div>
      <div class="chart-option">
        <label for="label-show">显示数据标签</label>
        <input type="checkbox" v-model="chartOptions.series.label.show">
        <span class="check"></span>
      </div>
    </div>
  </div>
</template>

<style scoped></style>