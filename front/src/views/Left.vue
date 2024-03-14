<script>
import axios from 'axios'
import * as XLSX from 'xlsx';

export default {
  emits: ['result', 'chartOptionsChanged'],
  name: 'left',
  data() {
    return {
      leftView: 'intro',
      file: null,
      allowFileExts: ['xls', 'xlsx', 'csv'],
      params: {
        data: null,
        filename: ''
      },
      uploadUrl: '/api/upload/',
      dataJson: null,
      keys: [],
      submitDisabled: true,
      indList: [],
      dependent: '',
      featureImportance: null,
    }
  },
  methods: {
    changeLeftView(view) {
      this.leftView = view
    },
    fileUpload() {
      this.file = this.$refs.uploadFile.files[0]
      let arr = this.file.name.split('.')
      let extension = arr[arr.length - 1]
      if (this.allowFileExts.indexOf(extension) < 0) {
        alert('文件格式不正确')
        this.$refs.uploadFile.value = ''
        this.file = null
        return
      }
      // read xlsx
      // fix the async problem
      if (extension === 'xlsx' || extension === 'xls') {
        let reader = new FileReader()
        reader.onload = (e) => {
          let data = new Uint8Array(e.target.result)
          let workbook = XLSX.read(data, { type: 'array' })
          let sheetName = workbook.SheetNames[0]
          let sheet = workbook.Sheets[sheetName]
          let json = XLSX.utils.sheet_to_json(sheet)
          this.dataJson = json

          this.params = {
            data: this.dataJson,
            filename: this.file.name
          }
          axios
            .post(this.uploadUrl, this.params)
            .then((response) => {
              this.keys = response.data.data
              this.indList = []
            })
            .catch((error) => {
              console.log(error)
            })
        }
        reader.readAsArrayBuffer(this.file)
      } else if (extension === 'csv') {
        let reader = new FileReader()
        reader.onload = (e) => {
          let data = e.target.result
          let workbook = XLSX.read(data, { type: 'binary' })
          let sheetName = workbook.SheetNames[0]
          let sheet = workbook.Sheets[sheetName]
          let json = XLSX.utils.sheet_to_json(sheet)
          this.dataJson = json

          this.params = {
            data: this.dataJson,
            filename: this.file.name
          }
          axios
            .post(this.uploadUrl, this.params)
            .then((response) => {
              this.keys = response.data.data
              this.indList = []
            })
            .catch((error) => {
              console.log(error)
            })
        }
        reader.readAsBinaryString(this.file)
      }
    },
    allOrNone() {
      let selectable = this.keys.filter((item) => {
        return this.dependent !== item
      })
      console.log(selectable)
      if (this.indList.length === selectable.length) {
        this.indList = []
      } else {
        this.indList = selectable
      }
    },
    submit() {
      axios
        .post('/api/submit/', {
          data: this.dataJson,
          dependent: this.dependent,
          indList: this.indList
        })
        .then((response) => {
          this.featureImportance = response.data.data
          // emit the data to the parent component
          this.$emit('result', this.featureImportance, this.chartOptions)
        })
        .catch((error) => {
          console.log(error)
        })
    }
  },
  watch: {
    indList(newVal, oldVal) {
      console.log("dependent", this.dependent)
      console.log("indList", this.indList)
      if (newVal.length > 0 && this.dependent !== '') {
        this.submitDisabled = false
      } else {
        this.submitDisabled = true
      }
    },
    dependent(newVal, oldVal) {
      if (this.indList.length > 0 && newVal !== '') {
        this.submitDisabled = false
      } else {
        this.submitDisabled = true
      }
    },
    immediate: true,
    deep: true
  },
}
</script>

<template>
  <!-- <div class="back back1" :class="leftView == 'intro' ? 'show' : ''"></div>
  <div class="back back2" :class="leftView == 'upload' ? 'show' : ''"></div> -->
  <div class="left-nav">
    <button @click="changeLeftView('intro')" class="left-nav-item" 
      :class="leftView == 'intro' ? 'active' : ''">使用说明</button>
    <button @click="changeLeftView('upload')" class="left-nav-item"
      :class="leftView == 'upload' ? 'active' : ''">文件上传</button>
  </div>
  <div class='left-show' v-if="leftView === 'intro'">
    <h2>使用说明</h2>
    <p>这是一个使用说明</p>
  </div>
  <div class='left-show' v-else-if="leftView === 'upload'">
    <h2>文件上传</h2>
    <div class="upload">
      <input class="file" type="file" @change="fileUpload" accept=".xls,.xlsx,.csv" ref="uploadFile">
    </div>
    <button class='submitt' @click="submit" :disabled="submitDisabled">提交</button>
    <div class="dep-select">
      <h3>选择因变量</h3>
      <div class="dep-selection" v-for="item in keys" :key="item">
        <label for="">{{ item }}</label>
        <input type="radio" :value="item" v-model="dependent" :disabled="indList.indexOf(item) >= 0">
      </div>
    </div>
    <div class="ind-select">
      <h3>选择自变量</h3>
      <button class="all-check" @click="allOrNone" v-if="keys.length > 0">全选</button>
      <div class="ind-selection" v-for="item in keys" :key="item">
        <label for="">{{ item }}</label>
        <input type="checkbox" :value="item" v-model="indList" :disabled="dependent == item">
        <span class="checkbox"></span>
      </div>
    </div>
  </div>
</template>
