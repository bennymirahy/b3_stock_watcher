import ativos from './db/ativos'
import { mockasync } from './mockutils'

export default {
  listAtivos (params) {
    let atvs = ativos
    if (params.name) {
      atvs = atvs.filter(x => {
        const searchStr = params.name.toUpperCase()
        return (x.name && x.name.toUpperCase().includes(searchStr))
      })
    }

    return mockasync({
      ativos: atvs,
      count: atvs.length
    }).then(response => response)
  }
}
