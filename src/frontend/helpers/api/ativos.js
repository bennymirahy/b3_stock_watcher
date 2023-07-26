/* eslint-disable no-unused-vars */
import { get, post } from './ajaxutils'

export default {
  listAtivos (params) {
    return get('/api/ativos/list', params).then(response => response.data)
  },
  fetchAtivosB3 (params) {
    return get('/api/ativos/fetch', { params }).then(response => response.data)
  },
  updateOrCreateAtivo (params) {
    return post(`/api/ativos/${params.sigla}/save`)
  },
  deleteAtivo (params) {
    return post(`/api/ativos/${params.sigla}/delete`)
  }
}
