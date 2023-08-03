<template>
  <v-dialog
    v-model="visible"
    max-width="90%"
    @click:outside="close()"
  >
    <v-container
      fluid
      style="background-color: linen;"
    >
      <v-flex pa-3>
        <LineChart
          :chart-data="chartData"
          :chart-options="chartOptions"
        />
      </v-flex>
    </v-container>
  </v-dialog>
</template>

<script>
import { Line as LineChart } from 'vue-chartjs'
import ChartAnnotationsPlugin from 'chartjs-plugin-annotation'
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement } from 'chart.js'
import api from '~api'

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement, ChartAnnotationsPlugin)
export default {
  components: { LineChart },
  props: {
    ativo: {
      type: Object,
      default: () => {}
    }
  },
  data () {
    return {
      history: [],
      visible: false,
      loading: false,
      chartOptions: {
        scales: {
          y: {
            title: {
              display: true,
              text: 'Cotação (R$)',
              font: {
                size: '21',
                weight: '700'
              }
            },
            grace: '20%',
            alignToPixels: true,
            ticks: {
              beginAtZero: true,
              font: {
                weight: '600'
              }
            },
            grid: {
              borderDash: [5],
              tickBorderDash: [5],
              display: true
            }
          },
          x: {
            ticks: {
              font: {
                weight: '600'
              }
            },
            grid: {
              borderDash: [5],
              tickBorderDash: [5],
              display: true
            },
            stacked: false
          }
        },
        plugins: {
          title: {
            display: true,
            text: `Histórico do Ativo ${this.ativo.sigla}`,
            font: {
              size: '28'
            }
          },
          legend: {
            display: false
          },
          annotation: {
            annotations: [{
              type: 'line',
              mode: 'horizontal',
              yMin: this.ativo.ref_price,
              yMax: this.ativo.ref_price,
              borderColor: 'rgb(75, 192, 192)',
              borderDash: [5],
              borderWidth: 4,
              label: {
                display: true,
                content: 'Preço de referência'
              }
            }]
          },
          tooltip: {
            enabled: true,
            boxPadding: 5,
            titleFont: {
              weight: 600,
              size: 16
            },
            bodyFont: {
              size: 16
            }
          }
        },
        elements: {
          point: {
            pointStyle: 'circle',
            borderColor: 'info'
          },
          line: {
            fill: true,
            borderColor: '#ff6347'
          }
        },
        responsive: true,
        maintainAspectRatio: false
      }
    }
  },
  computed: {
    chartData () {
      return {
        labels: this.history.map(hist => this.parseDate(hist.datetime)),
        datasets: [
          {
            backgroundColor: '#6a5acd',
            data: this.history.map(hist => Number(hist.price))
          }
        ]
      }
    },
    ref_price () {
      console.log(this.ativo.ref_price)
      return this.ativo.ref_price
    }
  },
  methods: {
    async getAtivoHistory () {
      this.loading = true
      try {
        const res = await api.ativos.listAtivoHistory(this.ativo.sigla)
        this.history = res.history
      } catch (err) {
        this.$store.commit('toast/open', { message: err.message, color: 'error' })
      } finally {
        this.loading = false
      }
    },
    parseDate (iso) {
      const dateObj = new Date(iso)
      return dateObj.toLocaleString('pt-BR', {
        hour: '2-digit',
        minute: '2-digit',
        day: '2-digit',
        month: '2-digit'
      })
    },
    close () {
      this.visible = false
    },
    openDialog () {
      this.visible = true
      this.getAtivoHistory()
    }
  }
}
</script>
