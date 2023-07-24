<template>
  <tr :key="ativo.id">
    <td>{{ ativo.sigla }}</td>
    <td>{{ ativo.parsedInterval }}</td>
    <td>{{ ativo.value }}</td>
    <td>{{ ativo.updated_at }}</td>
    <td>
      <v-icon
        slot="activator"
        left
        @click="openEditDialog()"
      >
        edit
      </v-icon>
      <v-icon
        slot="activator"
        left
        @click="openRemoveDialog()"
      >
        dangerous
      </v-icon>
    </td>
    <popup-criar-ativo
      ref="popupCriarAtivo"
      :ativo="ativo"
      :edit-mode="true"
      @reloadAtivos="reloadAtivos()"
    />
    <popup-remover-ativo
      ref="popupRemoverAtivo"
      :ativo="ativo"
      @reloadAtivos="reloadAtivos()"
    />
  </tr>
</template>

<script>
import popupCriarAtivo from '~/components/popup-criar-ativo'
import popupRemoverAtivo from '~/components/popup-remover-ativo'
export default {
  components: {
    popupCriarAtivo,
    popupRemoverAtivo
  },
  props: {
    ativo: {
      type: Object,
      default: () => {}
    }
  },
  methods: {
    openEditDialog () {
      this.$refs.popupCriarAtivo.openDialog()
    },
    openRemoveDialog () {
      this.$refs.popupRemoverAtivo.openDialog()
    },
    reloadAtivos () {
      this.$emit('reloadAtivos')
    }
  }
}
</script>
