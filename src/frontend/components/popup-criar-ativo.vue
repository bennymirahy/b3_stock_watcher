<template>
  <v-dialog
    v-model="visible"
    persistent
    width="500px"
    max-width="90%"
  >
    <v-card class="pa-4">
      <v-card-title class="title px-0 pt-2">
        {{ buttonActionText }} ativo
      </v-card-title>
      <v-card-text>
        <v-layout
          wrap
          justify-center
          class="px-0"
        >
          <v-flex
            sm12
            xs12
          >
            <v-autocomplete
              v-model="siglaTxt"
              label="Sigla*"
              :items="ativos"
              item-value="id"
              item-text="sigla"
              :filter="() => true"
              :loading="loadingAtivos"
              :search-input.sync="searchInputAtivos"
              :no-data-text="ativoNoDataText"
              placeholder="Digite a sigla do ativo..."
              :disabled="editMode"
              append-icon="search"
              class="mr-3"
              return-object
            />
          </v-flex>
          <v-flex
            align-center
            sm4
          >
            <vue-timepicker
              v-model="interval"
              label="Periodicidade de observação"
              format="HH:mm"
              :disabled="editMode"
              class="mr-3"
            />
          </v-flex>
          <v-flex xs12>
            <h3>Parâmetros de túnel</h3>
          </v-flex>
        </v-layout>
        <v-layout justify-space-between>
          <v-flex xs5>
            <v-text-field
              v-model="lowerLim"
              label="Limite inferior"
              hint="Limite inferior"
              style="min-width: 50px"
              prefix="-"
              type="number"
              suffix="%"
              single-line
            />
          </v-flex>
          <v-flex xs5>
            <v-text-field
              v-model="upperLim"
              label="Limite superior"
              hint="Limite inferior"
              style="min-width: 50px"
              prefix="+"
              type="number"
              suffix="%"
              single-line
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
            @click="editMode ? updateAtivo() : addAtivo()"
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
import 'vue2-timepicker/dist/VueTimepicker.css'
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
      ativos: [],
      interval: '',
      lowerLim: '',
      upperLim: '',
      siglaTxt: null,
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
    upperLim (txt) {
      console.log(txt)
    }
  },
  methods: {
    searchB3Ativos: debounce(async function ({ text = '', id = null }) {
      this.loadingAtivos = true
      try {
        this.ativos = await api.staff.listAtivos({ name: text, id })
        if (id) {
          this.siglaTxt = this.ativos[0]
        }
      } catch (err) {
        this.$store.commit('toast/open', { message: err.message, color: 'error' })
      } finally {
        this.loadingAtivos = false
      }
    }, 500),
    async addAtivo () {
      this.loadingAdd = true
      try {
        const params = this.dumpParams()
        const result = await api.ativo.addAtivo(params)
        this.$emit('reloadAtivos')
        if (result.success) {
          this.$store.commit('toast/open', {
            message: 'Ativo adicionado com sucesso',
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
    async updateAtivo () {
      this.loadingAdd = true
      try {
        const params = this.dumpParams()
        const result = await api.ativo.updateAtivo(params)
        this.$emit('reloadAtivos')
        if (result.success) {
          this.$store.commit('toast/open', {
            message: 'Ativo atualizado com sucesso',
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
        sigla: this.ativo.sigla,
        upper_lower: this.lowerLim,
        upper_limit: this.upperLim,
        interval: this.interval
      }
      return params
    },
    close () {
      this.visible = false
    },
    openDialog () {
      this.visible = true
      if (this.ativo) {
        this.interval = this.ativo.interval
        this.lowerLim = this.ativo.lower_limit
        this.upperLim = this.ativo.upper_limit
      }
    }
  }
}
</script>
