<template>
  <tr :key="ativo.id">
    <td>{{ ativo.sigla }}</td>
    <td>{{ ativo.interval }}</td>
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
    <v-btn color="primary">
      <v-icon
        left
        @click="openRemoveDialog()"
      >
        dangerous
      </v-icon>
    </v-btn>
    <popup-criar-ativo
      ref="popupCriarAtivo"
      :ativo="ativo"
      :edit-mode="true"
      @reloadAtivos="reloadAtivos()"
    />
  </tr>
</template>

<script>
import popupCriarAtivo from '~/components/popup-criar-ativo'
import 'material-design-icons-iconfont/dist/material-design-icons.css'
export default {
  components: {
    popupCriarAtivo
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
    openRemoveDialog () {
      this.$refs.popupRemoveAtivo.openDialog()
    },
    reloadAtivos () {
      this.$emit('reloadAtivos')
    }
  }
}
</script>
