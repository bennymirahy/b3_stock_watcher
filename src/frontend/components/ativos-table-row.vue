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
        @click="openDeleteDialog()"
      >
        dangerous
      </v-icon>
    </td>
    <popup-create-ativo
      ref="popupCreateAtivo"
      :ativo="ativo"
      :edit-mode="true"
      @reloadAtivos="reloadAtivos()"
    />
    <popup-delete-ativo
      ref="popupDeleteAtivo"
      :ativo="ativo"
      @reloadAtivos="reloadAtivos()"
    />
  </tr>
</template>

<script>
import popupCreateAtivo from '~/components/popup-create-ativo'
import popupDeleteAtivo from '~/components/popup-delete-ativo'
export default {
  components: {
    popupCreateAtivo,
    popupDeleteAtivo
  },
  props: {
    ativo: {
      type: Object,
      default: () => {}
    }
  },
  methods: {
    openEditDialog () {
      this.$refs.popupCreateAtivo.openDialog()
    },
    openDeleteDialog () {
      this.$refs.popupDeleteAtivo.openDialog()
    },
    reloadAtivos () {
      this.$emit('reloadAtivos')
    }
  }
}
</script>
