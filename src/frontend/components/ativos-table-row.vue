<template>
  <tr :key="ativo.id">
    <td>{{ ativo.sigla }}</td>
    <td>{{ ativo.parsedInterval }}</td>
    <td>{{ ativo.ref_price }}</td>
    <td>{{ ativo.updated_at }}</td>
    <td>
      <v-icon
        slot="activator"
        left
        @click="openPlotDialog()"
      >
        info
      </v-icon>
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
    <popup-ativo-plot
      ref="popupAtivoPlot"
      :ativo="ativo"
    />
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
import popupAtivoPlot from '~/components/popup-ativo-plot'
import popupCreateAtivo from '~/components/popup-create-ativo'
import popupDeleteAtivo from '~/components/popup-delete-ativo'
export default {
  components: {
    popupAtivoPlot,
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
    openPlotDialog () {
      this.$refs.popupAtivoPlot.openDialog()
    },
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
