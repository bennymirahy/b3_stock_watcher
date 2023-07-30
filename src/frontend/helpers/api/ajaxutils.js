import axios from 'axios'

axios.defaults.xsrfHeaderName = 'X-CSRFToken'
axios.defaults.xsrfCookieName = 'csrftoken'

export async function get (url, params) {
  const resp = await axios.get(url, { params })
  return resp
}

export async function post (url, data, config) {
  config = config || {}
  config.headers = config.headers || {}
  config.headers['Content-Type'] = 'application/json'
  const resp = await axios.post(url, data, config)
  return resp
}
