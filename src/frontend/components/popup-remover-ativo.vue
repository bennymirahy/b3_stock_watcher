<template>
  <v-dialog v-model="visible" width="500px" max-width="90%">
    <v-card class="pa-4">
      <v-card-title class="title px-0 pt-2">
        Remover - {{ ativo.name }}
      </v-card-title>
      <v-card-text>
        <v-layout wrap justify-center class="px-0">
          <v-flex xs12>
            <h3>Tem certeza que deseja parar de acompanhar esse ativo?</h3>
          </v-flex>
        </v-layout>
        <br>
        <v-layout wrap justify-center class="px-0" />
      </v-card-text>

      <v-layout justify-end>
        <v-flex text-xs-right>
          <v-btn color="error" @click="close()">
            Fechar
          </v-btn>
          <v-btn
            color="success"
            :loading="loading"
            @click="removerAtivo()"
          >
            Remover
          </v-btn>
        </v-flex>
      </v-layout>
    </v-card>
  </v-dialog>
</template>

<script>
import api from '~api'

export default {
  props: {
    ativo: {
      type: Object,
      default: () => {}
    }
  },
  data () {
    return {
      visible: false,
      loading: false
    }
  },
  methods: {
    async removerAtivo () {
      this.loading = true
      try {
        await api.staff.removerAtivo(this.ativo.id)
        this.$store.commit('toast/open', {
          message: ' ativo removido',
          color: 'success'
        })
      } catch (err) {
        this.$store.commit('toast/open', { message: err.message, color: 'error' })
      } finally {
        this.loading = false
        this.close()
      }
    },
    openDialog () {
      this.visible = true
    },
    close () {
      this.visible = false
    }
  }
}
</script>
