<template>
  <v-container fluid>
    <v-layout column>
      <v-flex
        class="px-1"
        xs12
      >
        <h1>Monitoramento de Ativos da B3</h1>
      </v-flex>

      <v-layout
        row
        wrap
        align-center
      >
        <v-flex
          class="px-2"
          grow
        >
          <v-text-field
            v-model="siglaSearch"
            append-icon="search"
            label="Buscar ativo"
            style="min-width: 200px"
            single-line
          />
        </v-flex>
        <v-btn
          color="primary"
          @click="openAddAtivoDialog()"
        >
          <v-icon> add </v-icon>Adicionar ativo
        </v-btn>
      </v-layout>
    </v-layout>
    <v-data-table
      :headers="headers"
      :items="ativos"
      :loading="loading"
      :server-items-length="totalItems"
      :items-per-page-options="rowsPerPageOptions"
      :pagination.sync="pagination"
      item-key="id"
      items-per-page-text="Registros por página"
    >
      <template #item="row">
        <ativos-table-row
          :key="row.item.id"
          :ativo="row.item"
          @reloadAtivos="update()"
        />
      </template>
    </v-data-table>

    <popup-criar-ativo
      ref="popupCriarAtivo"
      :edit-mode="false"
      @reloadAtivos="update()"
    />
  </v-container>
</template>

<script>
import debounce from 'lodash/debounce'
import api from '~api'
import ativosTableRow from '~/components/ativos-table-row'
import popupCriarAtivo from '~/components/popup-criar-ativo'
import 'material-design-icons-iconfont/dist/material-design-icons.css'

export default {
  components: {
    ativosTableRow,
    popupCriarAtivo
  },
  data () {
    return {
      ativos: [],
      loading: false,
      siglaSearch: '',
      headers: [
        { text: 'Sigla', value: 'sigla' },
        { text: 'Intervalo de Observação', value: 'parsedInterval' },
        { text: 'Último Valor (R$)', value: 'value' },
        { text: 'Última Atualização (UTC-3)', value: 'updated_at' },
        { text: 'Ações', value: 'acoes', sortable: false }
      ],
      rowsPerPageOptions: [
        10,
        20,
        50,
        { text: '$vuetify.dataIterator.rowsPerPageAll', value: -1 }
      ],
      pagination: {
        descending: false,
        page: 1,
        rowsPerPage: 20,
        sortBy: 'sigla'
      },
      totalItems: null
    }
  },
  watch: {
    pagination: {
      handler () {
        this.update()
      },
      deep: true
    },
    siglaSearch () {
      this.update()
    }
  },
  mounted () {
    this.update()
  },
  methods: {
    update: debounce(async function () {
      this.loading = true
      const params = this.dumpParams()
      try {
        const result = await api.ativos.listAtivos(params)
        console.log(result)
        this.ativos = this.parseAtivos(result.ativos)
        this.totalItems = result.count
      } catch (err) {
        this.$store.commit('toast/open', { message: err.message, color: 'error' })
      } finally {
        this.loading = false
      }
    }, 500),
    dumpParams () {
      const params = {
        sigla: this.siglaSearch,
        paginator: this.pagination
      }
      params.sigla = params.sigla.toUpperCase()
      return params
    },
    parseAtivos (ativos) {
      // Intervalos armazenados em minutos no banco de dados
      ativos.forEach(a => {
        if (a.parsedInterval) {
          return
        }
        if (a.interval > 60) {
          a.parsedInterval = a.interval / 60 + ' h'
        } else {
          a.parsedInterval = a.interval + ' min'
        }
      })
      return ativos
    },
    openAddAtivoDialog () {
      this.$refs.popupCriarAtivo.openDialog()
    }
  }
}
</script>
