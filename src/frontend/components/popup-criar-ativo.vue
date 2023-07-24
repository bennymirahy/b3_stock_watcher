<template>
  <v-dialog
    v-model="visible"
    persistent
    width="500px"
    max-width="90%"
    overlay-opacity="0.8"
    @click:outside="close()"
  >
    <v-card class="pa-6">
      <v-card-title class="title px-5 pt-2">
        {{ buttonActionText }} ativo
      </v-card-title>
      <v-card-text>
        <v-layout
          wrap
          justify-center
          class="px-0"
        >
          <v-flex xs12>
            <v-autocomplete
              v-model="siglaSelection"
              label="Sigla*"
              :items="ativos"
              item-value="id"
              item-text="sigla"
              :filter="() => true"
              :loading="loadingAtivos"
              :search-input.sync="searchInputAtivos"
              :no-data-text="ativoNoDataText"
              placeholder="Digite a sigla do ativo..."
              append-icon="search"
              class="mr-3"
              :disabled="editMode"
              return-object
            />
          </v-flex>
        </v-layout>
        <v-layout wrap py-3 justify-space-between>
          <v-flex xs12>
            <h3>Parâmetros de túnel</h3>
          </v-flex>
          <v-flex xs5>
            <v-text-field
              v-model="lowerLim"
              label="Limite inferior"
              hint="Limite inferior"
              style="min-width: 50px"
              type="number"
              suffix="%"
              single-line
              :rules="[rules.required, rules.between(-100, 0)]"
            />
          </v-flex>
          <v-flex xs5>
            <v-text-field
              v-model="upperLim"
              label="Limite superior"
              hint="Limite inferior"
              style="min-width: 50px"
              type="number"
              suffix="%"
              single-line
              :rules="[rules.required, rules.between(0, 100)]"
            />
          </v-flex>
        </v-layout>
        <v-layout wrap py-3 justify-space-between>
          <v-flex xs12 py-2>
            <h3>Periodicidade de observação</h3>
          </v-flex>
          <v-flex xs9 pr-2 class="align-self-end">
            <v-slider
              v-model="interval"
              min="1"
              :max="timeMax"
              label="Monitarar a cada"
              thumb-size="23"
              thumb-label="always"
            />
          </v-flex>
          <v-flex xs3>
            <v-select
              v-model="timeUnit"
              :items="timeUnitOptions"
              item-text="label"
              item-value="value"
            />
          </v-flex>
        </v-layout>
      </v-card-text>

      <v-layout justify-end>
        <v-flex text-xs-right>
          <v-btn
            color="error"
            @click="close()"
          >
            Fechar
          </v-btn>
          <v-btn
            color="success"
            :loading="loadingAdd"
            @click="createOrUpdateAtivo()"
          >
            {{ buttonActionText }}
          </v-btn>
        </v-flex>
      </v-layout>
    </v-card>
  </v-dialog>
</template>

<script>
import debounce from 'lodash/debounce'
import rules from '~/helpers/rules'
import api from '~api'

export default {
  props: {
    ativo: {
      type: Object,
      default: () => {}
    },
    editMode: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      visible: false,
      loadingAdd: false,
      loadingAtivos: false,
      loadingNoData: false,
      ativos: [this.ativo],
      timeUnitOptions: [
        { label: 'Minutos', value: 'minute', max: 60 },
        { label: 'Horas', value: 'hour', max: 24 }
      ],
      timeUnit: 'minute',
      interval: 5,
      lowerLim: -5,
      upperLim: 5,
      timeMax: 60,
      siglaSelection: this.ativo,
      searchInputAtivos: null,
      rules
    }
  },
  computed: {
    ativoNoDataText () {
      return this.loadingNoData ? 'Procurando...' : 'Nenhum resultado. Digite para procurar'
    },
    buttonActionText () {
      return this.editMode ? 'Editar' : 'Adicionar'
    }
  },
  watch: {
    searchInputAtivos (txt) {
      if (!txt || this.loadingAtivos || (this.ativo && txt === this.ativo.sigla)) {
        return
      }
      this.searchB3Ativos({ text: txt })
    },
    timeUnit (unit) {
      if (unit === 'hour') {
        this.timeMax = 24
      } else { this.timeMax = 60 }
    }
  },
  methods: {
    searchB3Ativos: debounce(async function ({ text = '' }) {
      this.loadingAtivos = true
      try {
        const result = await api.ativos.fetchAtivosB3({ sigla: text })
        this.ativos = result.ativos
      } catch (err) {
        this.$store.commit('toast/open', { message: err.message, color: 'error' })
      } finally {
        this.loadingAtivos = false
      }
    }, 500),
    async createOrUpdateAtivo () {
      this.loadingAdd = true
      try {
        const params = this.dumpParams()
        const result = await api.ativos.createOrUpdateAtivo(params)
        this.$emit('reloadAtivos')
        if (result.success) {
          const acao = this.editMode ? 'atualizado' : 'adicionado'
          this.$store.commit('toast/open', {
            message: `Ativo ${acao} com sucesso`,
            color: 'success'
          })
        }
      } catch (err) {
        this.$store.commit('toast/open', { message: err.message, color: 'error' })
      } finally {
        this.loadingAdd = false
        this.close()
      }
    },
    dumpParams () {
      const params = {
        sigla: this.siglaSelection,
        upper_lower: this.lowerLim,
        upper_limit: this.upperLim,
        interval: this.timeUnit === 'minute' ? this.interval : this.interval * 60
      }
      return params
    },
    setAtivoData () {
      this.ativos.push(this.ativo)
      this.siglaSelection = this.ativo
      this.interval = this.ativo.parsedInterval.split(' ')[0]
      this.timeUnit = this.ativo.parsedInterval.split(' ')[1] === 'min' ? 'minute' : 'hour'
      this.lowerLim = this.ativo.lower_limit
      this.upperLim = this.ativo.upper_limit
    },
    close () {
      this.visible = false
    },
    openDialog () {
      this.visible = true
      if (this.ativo) {
        this.setAtivoData()
        console.log(this.siglaSelection)
      }
    }
  }
}
</script>
