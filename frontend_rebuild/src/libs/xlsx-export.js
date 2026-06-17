import writeXlsxFile from 'write-excel-file/browser'

const headerCell = (value) => ({
  value,
  fontWeight: 'bold'
})

const normalizeValue = (value) => {
  if (value == null) return ''
  if (value instanceof Date) return value
  if (Array.isArray(value)) return value.join(' | ')
  if (typeof value === 'object') return JSON.stringify(value)
  return value
}

const rowsToSheetData = (rows) => {
  if (!rows?.length) return []

  const headers = Array.from(
    rows.reduce((keys, row) => {
      Object.keys(row || {}).forEach((key) => keys.add(key))
      return keys
    }, new Set())
  )

  if (!headers.length) return []

  return [
    headers.map(headerCell),
    ...rows.map(row => headers.map(key => normalizeValue(row?.[key])))
  ]
}

export const exportWorkbook = async (sheets, fileName) => {
  const workbookSheets = sheets.map(({ name, rows }) => ({
    sheet: name,
    data: rowsToSheetData(rows)
  }))

  await writeXlsxFile(workbookSheets).toFile(fileName)
}
