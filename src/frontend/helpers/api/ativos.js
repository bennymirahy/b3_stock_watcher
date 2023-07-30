/* eslint-disable no-unused-vars */
import { get, post } from './ajaxutils'

export default {
  listAtivos (params) {
    return get('/api/ativos/list', params).then(response => response.data)
  },
  fetchAtivosB3 (params) {
    return get('/api/ativos/fetch', params).then(response => response.data)
  },
  updateOrCreateAtivo (sigla, params) {
    return post(`/api/ativos/${sigla}/save`, params).then(response => response.data)
  },
  deleteAtivo (sigla) {
    return post(`/api/ativos/${sigla}/delete`).then(response => response.data)
  }
}
