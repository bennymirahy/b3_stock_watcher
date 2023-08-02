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
      :options.sync="pagination"
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

    <popup-create-ativo
      ref="popupCreateAtivo"
      :edit-mode="false"
      @reloadAtivos="update()"
    />
    <LoginDialog ref="LoginDialog" />
  </v-container>
</template>

<script>
import debounce from 'lodash/debounce'
import api from '~api'
import ativosTableRow from '~/components/ativos-table-row'
import popupCreateAtivo from '~/components/popup-create-ativo'
import 'material-design-icons-iconfont/dist/material-design-icons.css'

export default {
  components: {
    ativosTableRow,
    popupCreateAtivo
  },
  data () {
    return {
      ativos: [],
      loading: false,
      siglaSearch: '',
      headers: [
        { text: 'Sigla', value: 'sigla' },
        { text: 'Frequência de observação', value: 'parsedInterval', sortable: false },
        { text: 'Preço de referência (R$)', value: 'ref_price', sortable: false },
        { text: 'Última atualização (UTC-3)', value: 'updated_at' },
        { text: 'Ações', value: 'acoes', sortable: false }
      ],
      rowsPerPageOptions: [
        10,
        20,
        50,
        { text: '$vuetify.dataIterator.rowsPerPageAll', value: -1 }
      ],
      pagination: {
        page: 1,
        itemsPerPage: 10,
        sortBy: ['sigla']
      },
      totalItems: null
    }
  },
  computed: {
    loggedIn () {
      return this.$store.getters['auth/loggedIn']
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
    },
    loggedIn () {
      this.update()
    }
  },
  mounted () {
    if (this.loggedIn === false) {
      this.openLoginDialog()
    } else {
      this.update()
    }
  },
  methods: {
    update: debounce(async function () {
      this.loading = true
      const params = this.dumpParams()
      try {
        const result = await api.ativos.listAtivos(params)
        this.ativos = this.parseAtivos(result.ativos)
        this.totalItems = result.count
      } catch (err) {
        if (!err.includes('401')) {
          this.$store.commit('toast/open', { message: err.message, color: 'error' })
        }
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
      this.$refs.popupCreateAtivo.openDialog()
    },
    openLoginDialog () {
      this.$refs.LoginDialog.open()
    }
  }
}
</script>
