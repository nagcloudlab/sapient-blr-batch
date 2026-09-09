{{- define "todos-app.name" -}}
{{ .Release.Name }}-{{ .Chart.Name }}
{{- end }}

{{- define "todos-app.labels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}
