import formHelpers from './forms'

const rules = {
  required (value) {
    return (value !== null && value !== undefined && value !== '') || 'Campo obrigatório'
  },
  objectRequired (value) {
    return (value && !!Object.keys(value).length) || 'Campo obrigatório'
  },
  defined (value) {
    return value !== undefined || 'Campo obrigatório'
  },
  onlyNumbers (value) {
    const message = 'Somente números'
    if (!value) {
      return message
    }
    if (typeof value !== 'string') {
      value = String(value)
    }
    const valid = value.match(/^[0-9]+$/) !== null
    return valid || message
  },
  atLeastOneSelected (selectedList) {
    return selectedList.length > 0 || 'Ao menos um item deve ser selecionado'
  },
  regex (regexx) {
    return value => {
      const message = 'O valor está inválido'
      if (!value) {
        return message
      }
      const valid = value.match(regexx) !== null
      return valid || message
    }
  },
  not_empty (value) {
    return (value.length && value.length > 0) || 'Campo obrigatório'
  },
  taf_or_estadual_must_exist (prop1, prop2) {
    const message = 'Precisa ter ou TAF ou Registro Estadual'
    return (prop1 !== '' || prop2 !== '') || message
  },
  minlen (m) {
    return v => {
      if (v === undefined || v === null) {
        return true
      }
      v = v.toString()
      return v.length >= m || `Digite pelo menos ${m} caracteres`
    }
  },
  maxlen (m) {
    return v => {
      if (v === undefined || v === null) {
        return true
      }
      v = v.toString()
      return v.length <= m || `Máximo de ${m} caracteres`
    }
  },
  email (value, required = true) {
    if (!required && !value) {
      return true
    }
    const email = value && value.trim()
    const valid = formHelpers.isValidEmail(email)
    return valid || 'Digite um e-mail válido.'
  },
  ddmmyyyy (value) {
    if (value === undefined || value === null) {
      return true
    }
    value = value.toString()
    const message = 'Digite uma data no formato ddmmyyyy'
    const pattern = /^([0-9]{8})$/
    if (value.length !== 8 || !pattern.test(value)) {
      return message
    }
    const [d, m, y] = [value.substring(0, 2), value.substring(2, 4), value.substring(4, 8)]
    if (d > 31 || m > 12 || y > 2100) {
      return message
    }
    return true
  },
  password (value) {
    const message = 'A senha deve conter pelo menos 8 caracteres'
    const valid = formHelpers.isValidPassword(value)
    return valid || message
  },
  between (start, end) {
    return value => {
      if (value === undefined || value === null) {
        return true
      }
      const message = `Valor deve estar entre ${start} e ${end}`
      if (formHelpers.isValidCurrency(value)) {
        value = formHelpers.moedaToFloat(value)
      }
      const valid = value >= start && value <= end
      return valid || message
    }
  },
  money (value) {
    const message = 'O valor inválido. Ex. válido: 1.500,90'
    const valid = formHelpers.isValidCurrency(value)
    return valid || message
  },
  percent (value) {
    const message = 'O valor inserido é inválido. Exemplo de entrada válida: 50,00'
    const valid = formHelpers.isValidCurrency(value)
    return valid || message
  },
  duration (value) {
    const message = 'O valor inválido. Ex. válido: 6:35'
    if (!value) {
      return true
    }
    const valid = !!value.match(/^[0-9]+:[0-9]{2}$/)
    return valid || message
  },
  minDurationMinutes (minMinutes) {
    return v => {
      const minMilli = minMinutes * 60 * 1000
      const minStr = formHelpers.duracaoToStr(minMilli)
      const valueMilli = formHelpers.duracaoToMilli(v)
      if (!valueMilli || valueMilli < minMilli) {
        return `Valor mínimo: ${minStr}`
      }
      return true
    }
  },
  greaterThan (vmin) {
    const message = `Valor deve ser maior que ${vmin}`
    return value => {
      if (value === undefined || value === null) {
        return message
      }
      value = value.toString()
      if (formHelpers.isValidCurrency(value)) {
        value = formHelpers.moedaToFloat(value)
      } else {
        value = value.replace(',', '.')
      }
      const valid = value > vmin
      return valid || message
    }
  },
  greaterThanOrEqual (vmin) {
    const message = `Valor deve ser maior ou igual a ${vmin}`
    return value => {
      if (value === undefined || value === null) {
        return message
      }
      value = value.toString()
      if (formHelpers.isValidCurrency(value)) {
        value = formHelpers.moedaToFloat(value)
      } else {
        value = value.replace(',', '.')
      }
      const valid = value >= vmin
      return valid || message
    }
  },
  greaterThanOrEqualOrNull (vmin) {
    const message = `Valor deve ser maior ou igual a ${vmin}`
    return value => {
      if (value === undefined) {
        return message
      }
      if (value === null) {
        value = vmin
      }
      value = value.toString()
      if (formHelpers.isValidCurrency(value)) {
        value = formHelpers.moedaToFloat(value)
      } else {
        value = value.replace(',', '.')
      }
      const valid = parseFloat(value) >= parseFloat(vmin)
      return valid || message
    }
  },
  greaterThanOrEqualNotRequired (vmin) {
    const message = `Valor deve ser maior ou igual a ${vmin}`
    return value => {
      if (value === undefined || value === null) {
        value = vmin
      }
      value = value.toString()
      if (formHelpers.isValidCurrency(value)) {
        value = formHelpers.moedaToFloat(value)
      } else {
        value = value.replace(',', '.')
      }
      const valid = parseFloat(value) >= parseFloat(vmin)
      return valid || message
    }
  },
  lessThanOrEqual (vmax) {
    const message = `Valor deve ser menor ou igual a ${vmax}`
    return value => {
      if (value === undefined || value === null) {
        return message
      }
      value = value.toString()
      if (formHelpers.isValidCurrency(value)) {
        value = formHelpers.moedaToFloat(value)
      } else {
        value = value.replace(',', '.')
      }
      const valid = value <= vmax
      return valid || message
    }
  },
  alphanumeric (value) {
    if (value === undefined || value === null) {
      return true
    }
    return value.match(/^[a-z0-9]+$/i) !== null || 'Apenas letras e números'
  },
  number (value) {
    if (value === undefined || value === null) {
      return true
    }
    return `${value}`.match(/^[0-9]*$/i) !== null || 'Apenas números'
  },
  onlyNumbersOrNull (value) {
    if (value === undefined) {
      return true
    }
    if (value === null) {
      return false
    }
    return `${value}`.match(/^[0-9]*$/i) !== null || 'Apenas números'
  },
  text (value) {
    if (!value) {
      return true
    }
    return `${value}`.match(/^[a-z]*$/i) !== null || 'Apenas letras'
  },
  textAndSpaceAndAccent (value) {
    if (!value) {
      return true
    }
    return `${value}`.match(/^[a-zA-Z\u00C0-\u00FF ]*$/i) !== null || 'Apenas letras e espaços'
  },
  textAndSpaceAndAccentInArray (valuesList) {
    let valid = true
    const message = 'Apenas letras e espaços'
    if (!valuesList) {
      valid = false
    }
    valuesList.forEach(value => {
      if (`${value}`.match(/^[a-zA-Z\u00C0-\u00FF ]*$/i) === null) {
        valid = false
      }
    })
    return valid || message
  },
  decimalNumber (value) {
    if (value === undefined || value === null) {
      return true
    }
    return `${value}`.match(/^[+-]?([0-9]+\.?[0-9]*|\.[0-9]+)$/i) != null || 'Número decimal com ponto'
  },
  exactLength (len) {
    return value => {
      if (value === undefined || value === null) {
        return true
      }
      value = value.toString()
      return value.length === len || `Campo deve ter exatamente ${len} caracteres`
    }
  },
  lengthNumbers (len) {
    return value => {
      const message = `O valor deve conter ${len} dígitos`
      if (!value) {
        return message
      }
      const valid = (!!value && value.length === len)
      return valid || message
    }
  },
  lengthBetween (min, max) {
    const message = `O valor deve ter entre ${min} e ${max} caracteres.`
    return value => {
      const valid = value && value.length >= min && value.length <= max
      return valid || message
    }
  },
  listHorariosComDeltaDias (value) {
    if (!value) {
      return true
    }
    const message = 'Os horários devem estar separados por espaço e no formato HH:HH, HH:HH-d ou HH:HH+d'
    const horarios = value.split(' ')
    const regexHorarioComDeltaDias = /^([0-1][0-9]|[2][0-3]):([0-5][0-9])([+|-]?[0-9]+)?$/
    const valid = horarios.every(elem => regexHorarioComDeltaDias.test(elem))
    return valid || message
  },
  listGruposId (value) {
    if (!value) {
      return true
    }
    const message = 'Os ids devem estar separados por espaço. Somente números são aceitos.'
    const gruposId = value.split(' ')
    const regexGruposId = /[0-9]/
    const valid = gruposId.every(elem => regexGruposId.test(elem))
    return valid || message
  },
  isPositiveNumber (numberValue) {
    const message = 'Valor não pode ser negativo'
    if (numberValue && numberValue.includes('-')) {
      return message
    }
    return true
  }
}

rules.mergeRules = otherRules => {
  return Object.assign({}, rules, otherRules)
}

export default rules
