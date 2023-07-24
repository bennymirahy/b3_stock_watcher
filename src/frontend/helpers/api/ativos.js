/* eslint-disable no-unused-vars */
import { get, post } from './ajaxutils'

export default {
  listAtivos (params) {
    return get('/api/ativos/list', { params }).then(response => response.data)
  }
}
