export default {
  isValidEmail (email) {
    if (!email) {
      return false
    }
    return email.toLowerCase().match(/[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}/) !== null
  },
  isValidPhone (phone) {
    if (!phone || phone.length < 8) {
      return false
    }
    return phone.match(/^[0-9\-\s()]+$/) !== null
  },
  isInternationalPhone (phone) {
    if (!phone || phone.length < 8) {
      return false
    }
    return phone.match(/^\+[0-9\-\s()]+$/) !== null
  },
  isValidPassword (password) {
    const valid = (password && password.length >= 8)
    return valid
  },
  canConvertStrToDecimal (value) {
    const formatted = String(value).replace(',', '.')
    return formatted.match(/^[0-9]+(\.[0-9]{2})?$/) !== null
  },
  isValidCurrency (value) {
    if (!value) {
      return true
    }
    value = value.toString()
    return value.match(/^[0-9]{1,3}(\.[0-9]{1,3})*,[0-9]{2}$/) !== null
  },
  moedaToFloat (value) {
    if (value === null || value === undefined) {
      return
    }
    value = value.toString()
    let signal = '+'
    if (value && '-+'.includes(value[0])) {
      signal = value[0]
      value = value.slice(1)
    }
    const cents = value.replace(/[^0-9]/g, '') || 0
    return Number(`${signal}${cents}`) / 100.0
  },
  moedaToTax (value) {
    if (value === null || value === undefined) {
      return
    }
    value = value.toString()
    let signal = '+'
    if (value && '-+'.includes(value[0])) {
      signal = value[0]
      value = value.slice(1)
    }
    const cents = value.replace(/[^0-9]/g, '') || 0
    return Number(`${signal}${cents}`) / 10000.0
  },
  trimSpaces (string) {
    if (!string) {
      return
    }
    return string.trim().replace(/\s+/g, ' ')
  }
}
