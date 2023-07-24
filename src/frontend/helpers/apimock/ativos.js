import ativos from './db/ativos'
import indexes from './db/indexes'
import { mockasync } from './mockutils'

export default {
  listAtivos (params) {
    let atvs = ativos
    if (params.sigla) {
      const searchStr = params.sigla.toUpperCase()
      atvs = atvs.filter(x => {
        return (x.sigla && x.sigla.toUpperCase().includes(searchStr))
      })
    }

    return mockasync({
      ativos: atvs,
      count: atvs.length
    }).then(response => response)
  },
  fetchAtivosB3 (params) {
    let idx = indexes.map(x => ({ sigla: x }))
    if (params.sigla) {
      const searchStr = params.sigla.toUpperCase()
      idx = idx.filter(x => {
        return (x.sigla && x.sigla.toUpperCase().includes(searchStr))
      })
    }
    console.log(idx)

    return mockasync({
      ativos: idx,
      count: idx.length
    }).then(response => response)
  },
  createOrUpdateAtivo () {
    return mockasync({
      success: true
    })
  },
  removerAtivo () {
    return mockasync({
      success: true
    })
  }
}
