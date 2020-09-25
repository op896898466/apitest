<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-lx-calendar"></i> 用例管理</el-breadcrumb-item>
                <el-breadcrumb-item>编辑用例</el-breadcrumb-item>
            </el-breadcrumb>
        </div>

        <div class="container">
            <el-form>
                <el-row :gutter="20">
                    <el-col :span="24">
                        <el-form-item label="选择配置">
                            <el-select v-model="selected_configure_id" clearable placeholder="请选择"
                                    @change="getConfigureDetail(selected_configure_id)">
                                <el-option v-for="(item, key) in configures" :key="key" :label="item.name"
                                        :value="item.id">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>
            </el-form>
            <el-tabs type="border-card">
                <el-tab-pane label="基本信息">
                    <div class="form-box">
                        <el-form label-position="left" label-width="80px">
                            <el-row :gutter="20">
                                <el-col :span="24">
                                    <el-form-item label="选择项目">
                                        <el-select v-model="selected_project_id" placeholder="请选择"
                                                   @change="switchProject">
                                            <el-option v-for="(item, key) in project_names" :key="key"
                                                       :label="item.name" :value="item.id">
                                            </el-option>
                                        </el-select>
                                    </el-form-item>
                                </el-col>
                            </el-row>

                            <el-row :gutter="20">
                                <el-col :span="12">
                                    <el-form-item label="选择模块">
                                        <el-select v-model="choose_selected_module_id" placeholder="请选择"
                                                   @change="getTestcaseByModuleID(choose_selected_module_id)">
                                            <el-option v-for="(item, key) in choose_modules" :key="key" :label="item.name"
                                                       :value="item.id">
                                            </el-option>
                                        </el-select>
                                    </el-form-item>
                                </el-col>

                                <!-- <el-col :span="12">
                                    <el-form-item label="选择配置">
                                        <el-select v-model="selected_configure_id" placeholder="请选择" clearable>
                                            <el-option v-for="(item, key) in configures" :key="key" :label="item.name"
                                                       :value="item.id">
                                            </el-option>
                                        </el-select>
                                    </el-form-item>
                                </el-col> -->

                            </el-row>

                            <el-row :gutter="350">
                                <el-col :span="12" class="drag-box-col">
                                    <div class="drag-box-item">
                                        <div class="item-title">待选前置用例</div>
                                        <draggable v-model="unselected" :options="dragOptions">
                                            <transition-group tag="div" class="item-ul">
                                                <div v-for="item in unselected" class="drag-list" :key="item.id">
                                                    {{ item.name }}
                                                </div>
                                            </transition-group>
                                        </draggable>
                                    </div>
                                </el-col>

                                <el-col :span="12" class="drag-box-col">
                                    <div class="drag-box-item">
                                        <div class="item-title">已选前置用例</div>
                                        <draggable v-model="selected_testcase" :options="dragOptions" @change="changeResult()">
                                            <transition-group tag="div" class="item-ul">
                                                <div v-for="item in selected_testcase" class="drag-list" :key="item.id">
                                                    {{ item.name }}
                                                </div>
                                            </transition-group>
                                        </draggable>
                                    </div>
                                </el-col>

                                <!-- <el-col :span="12" class="drag-box-col">
                                    <div class="drag-box-item">
                                        <div class="item-title">已选后置用例</div>
                                        <draggable v-model="selected_testcase_after" :options="dragOptions" @change="changeResultAfter()">
                                            <transition-group tag="div" class="item-ul">
                                                <div v-for="item in selected_testcase_after" class="drag-list" :key="item.id">
                                                    {{ item.name }}
                                                </div>
                                            </transition-group>
                                        </draggable>
                                    </div>
                                </el-col> -->

                            </el-row>

                        </el-form>
                    </div>
                </el-tab-pane>

                <el-tab-pane label="请求信息">
                    <!--<div class="form-box">-->
                        <el-form style="margin: 0 0 0 10px">

                            <el-form-item>
                                <el-input placeholder="Enter request URL"
                                          v-model="apiMsgData.url"
                                          class="input-with-select"
                                          style="width: 80%;margin-right: 5px">
                                    <el-select v-model="apiMsgData.method"
                                               size="medium"
                                               style="width: 100px"
                                               slot="prepend"
                                               placeholder="选择请求方式">
                                        <el-option v-for="item in methods"
                                                   :key="item"
                                                   :value="item"
                                                   :label="item">
                                        </el-option>
                                    </el-select>
                                    <el-button
                                            slot="append"
                                            type="primary"
                                            @click="ParamViewStatus = !ParamViewStatus">
                                        Params
                                    </el-button>
                                </el-input>
                            </el-form-item>
                        </el-form>

                        <el-table :data="apiMsgData.param"
                                  :row-style="{'background-color': 'rgb(250, 250, 250)'}"
                                  style="width:98.2%;margin-top:-20px;left: 10px;"
                                  size="mini"
                                  :show-header="false"
                                  v-show="this.ParamViewStatus">
                            <el-table-column property="key" label="Key" header-align="center" min-width="80">
                                <template slot-scope="scope">
                                    <el-input v-model="scope.row.key" size="mini" placeholder="key">
                                    </el-input>
                                </template>
                            </el-table-column>
                            <el-table-column property="value" label="Value" header-align="center" min-width="200">
                                <template slot-scope="scope">
                                    <el-input v-model="scope.row.value"
                                              size="mini" placeholder="value"
                                              :id="'param_input' + scope.$index "
                                              type="textarea"
                                              rows=1
                                              @focus="showLine('param_input', scope.$index)"
                                              @input="changeLine()"
                                              @blur="resetLine(scope.$index)"
                                              resize="none"
                                    >
                                    </el-input>
                                </template>
                            </el-table-column>
                            <el-table-column property="value" label="操作" header-align="center" width="60">
                                <template slot-scope="scope">
                                    <el-button type="danger"
                                               icon="el-icon-delete"
                                               size="mini"
                                               @click.native="delTableRow('param',scope.$index)">
                                    </el-button>
                                </template>
                            </el-table-column>
                        </el-table>

                        <el-tabs style="margin: 0 0 0 10px" v-model="bodyShow">
                            <el-tab-pane label="Headers" name="first">
                                <el-table :data="apiMsgData.header" size="mini" stripe :show-header="false"
                                          class="h-b-e-a-style"
                                          :row-style="{'background-color': 'rgb(250, 250, 250)'}">
                                    <el-table-column property="key" label="Key" header-align="center" minWidth="100">
                                        <template slot-scope="scope">
                                            <el-input v-model="scope.row.key" size="mini" placeholder="key">
                                            </el-input>
                                        </template>
                                    </el-table-column>

                                    <el-table-column property="value" label="Value" header-align="center" minWidth="200">
                                        <template slot-scope="scope">
                                            <el-input v-model="scope.row.value" size="mini" placeholder="value">
                                            </el-input>
                                        </template>
                                    </el-table-column>
                                    <el-table-column property="value" label="操作" header-align="center" width="80">
                                        <template slot-scope="scope">
                                            <el-button type="danger" icon="el-icon-delete" size="mini"
                                                       @click.native="delTableRow('header',scope.$index)">
                                            </el-button>
                                        </template>
                                    </el-table-column>
                                </el-table>
                            </el-tab-pane>
                            <el-tab-pane label="Body" name="second" :disabled="apiMsgData.method === 'GET'">
                                <el-form :inline="true" class="demo-form-inline" style="margin-top: 10px">
                                    <el-radio-group v-model="apiMsgData.choiceType">
                                        <el-radio label="data">form-data</el-radio>
                                        <el-radio label="files">files</el-radio>
                                        <el-radio label="json">json</el-radio>
                                        <!--<el-radio label="text">text</el-radio>-->
                                    </el-radio-group>
                                    <el-button type="primary" size="mini"
                                               v-show="apiMsgData.choiceType === 'json'"
                                               style="margin-left:20px"
                                               @click="formatData()">格式化

                                    </el-button>
                                </el-form>
                                <hr style="height:1px;border:none;border-top:1px solid rgb(241, 215, 215);"/>

                                <div v-if="apiMsgData.choiceType === 'json'">
                                    <div style="border:1px solid rgb(234, 234, 234) ">
                                        <el-container>
                                            <editor
                                                    style="font-size: 15px"
                                                    v-model="apiMsgData.jsonVariable"
                                                    @init="editorInit"
                                                    lang="json"
                                                    theme="chrome"
                                                    width="100%"
                                                    height="575px"
                                                    :options="{}"
                                            >
                                            </editor>
                                        </el-container>

                                    </div>
                                </div>
                                <el-table :data="apiMsgData.variable"
                                          size="mini"
                                          stripe
                                          :show-header="false" height="500"
                                          style="background-color: rgb(250, 250, 250)"
                                          v-if="apiMsgData.choiceType === 'data'"
                                          :row-style="{'background-color': 'rgb(250, 250, 250)'}">
                                    <el-table-column label="Key" header-align="center" minWidth="100">
                                        <template slot-scope="scope">
                                            <el-input v-model="scope.row.key" size="mini" placeholder="key">
                                            </el-input>
                                        </template>
                                    </el-table-column>
                                    <el-table-column label="type" header-align="center" width="100">
                                        <template slot-scope="scope">
                                            <el-select v-model="scope.row.param_type" size="mini">
                                                <el-option v-for="item in paramTypes" :key="item" :value="item">
                                                </el-option>
                                            </el-select>
                                        </template>
                                    </el-table-column>
                                    <el-table-column label="Value" header-align="center" minWidth="200">
                                        <template slot-scope="scope">
                                            <div>
                                                <el-input v-model="scope.row.value"
                                                          :id="'data_input' + scope.$index "
                                                          type="textarea"
                                                          rows=1
                                                          @focus="showLine('data_input', scope.$index)"
                                                          @input="changeLine()"
                                                          @blur="resetLine()"
                                                          size="mini"
                                                          resize="none" placeholder="value">
                                                </el-input>
                                            </div>

                                        </template>
                                    </el-table-column>

                                    <el-table-column property="value" label="操作" header-align="center" width="80">
                                        <template slot-scope="scope">
                                            <el-button type="danger" icon="el-icon-delete" size="mini"
                                                       @click.native="delTableRow('variable',scope.$index)">
                                            </el-button>
                                        </template>
                                    </el-table-column>
                                </el-table>

                                <div v-if="apiMsgData.choiceType === 'files'">
                                <el-upload
                                class="upload-demo"
                                :action="uploadUrl"
                                :headers="headers"
                                :on-change="handleChange"
                                :on-remove="handleRemove"
                                drag
                                multiple        
                                :file-list="apiMsgData.filesVariable"               
                                >
                                <i class="el-icon-upload"></i>
                                <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                                </el-upload>

                                
                                </div>

                            </el-tab-pane>
                            <el-tab-pane label="Extract" name="third">
                                <el-table :data="apiMsgData.extract" size="mini" stripe :show-header="false"
                                          class="h-b-e-a-style"
                                          :row-style="{'background-color': 'rgb(250, 250, 250)'}">
                                    <el-table-column property="key" label="Key" header-align="center" minWidth="100">
                                        <template slot-scope="scope">
                                            <el-input v-model="scope.row.key" size="mini" placeholder="key">
                                            </el-input>
                                        </template>
                                    </el-table-column>
                                    <el-table-column property="value" label="Value" header-align="center" minWidth="200">
                                        <template slot-scope="scope">
                                            <el-input v-model="scope.row.value" size="mini" placeholder="value">
                                            </el-input>
                                        </template>
                                    </el-table-column>
                                    <el-table-column property="value" label="操作" header-align="center" width="80">
                                        <template slot-scope="scope">
                                            <el-button type="danger" icon="el-icon-delete" size="mini"
                                                       @click.native="delTableRow('extract',scope.$index)">
                                            </el-button>
                                        </template>
                                    </el-table-column>
                                </el-table>
                            </el-tab-pane>
                            <el-tab-pane label="Assert" name="fourth">
                                <el-table :data="apiMsgData.validate" size="mini" stripe :show-header="false"
                                          class="h-b-e-a-style"
                                          :row-style="{'background-color': 'rgb(250, 250, 250)'}">

                                    <el-table-column property="key" label="Key" header-align="center" minWidth="100">
                                        <template slot-scope="scope">
                                            <el-input v-model="scope.row.key" size="mini" placeholder="check">
                                            </el-input>
                                        </template>
                                    </el-table-column>
                                    <el-table-column label="Comparator" header-align="center" width="200">
                                        <template slot-scope="scope">
                                            <el-autocomplete
                                                    class="inline-input"
                                                    v-model="scope.row.comparator"
                                                    :fetch-suggestions="querySearch"
                                                    placeholder="请选择"
                                                    size="mini"
                                            ></el-autocomplete>
                                        </template>
                                    </el-table-column>
                                    <el-table-column label="type" header-align="center" width="100">
                                        <template slot-scope="scope">
                                            <el-select v-model="scope.row.param_type" size="mini">
                                                <el-option v-for="item in paramTypes" :key="item" :value="item">
                                                </el-option>
                                            </el-select>
                                        </template>
                                    </el-table-column>
                                    <el-table-column property="value" label="Value" header-align="center" minWidth="200">
                                        <template slot-scope="scope">
                                            <el-input v-model="scope.row.value" size="mini" placeholder="expected">
                                            </el-input>
                                        </template>
                                    </el-table-column>
                                    <el-table-column property="value" label="操作" header-align="center" width="80">
                                        <template slot-scope="scope">
                                            <el-button type="danger" icon="el-icon-delete" size="mini"
                                                       @click.native="delTableRow('validate',scope.$index)">
                                            </el-button>
                                        </template>
                                    </el-table-column>
                                </el-table>
                            </el-tab-pane>
                        </el-tabs>

                    <!--</div>-->
                </el-tab-pane>

                <el-tab-pane label="环境变量|参数化|请求钩子|skip">

                    <el-tabs style="margin: 0 0 0 10px" v-model="otherShow">
                        <el-tab-pane label="环境变量" name="first">
                            <el-table :data="apiMsgData.globalVar" size="mini" stripe :show-header="false"
                                      class="h-b-e-a-style"
                                      :row-style="{'background-color': 'rgb(250, 250, 250)'}">
                                <el-table-column property="key" label="Key" header-align="center" minWidth="100">
                                    <template slot-scope="scope">
                                        <el-input v-model="scope.row.key" size="mini" placeholder="key">
                                        </el-input>
                                    </template>
                                </el-table-column>

                                <el-table-column label="type" header-align="center" width="100">
                                    <template slot-scope="scope">
                                        <el-select v-model="scope.row.param_type" size="mini">
                                            <el-option v-for="item in paramTypes" :key="item" :value="item">
                                            </el-option>
                                        </el-select>
                                    </template>
                                </el-table-column>

                                <el-table-column property="value" label="Value" header-align="center" minWidth="200">
                                    <template slot-scope="scope">
                                        <el-input v-model="scope.row.value" size="mini" placeholder="value">
                                        </el-input>
                                    </template>
                                </el-table-column>
                                <el-table-column property="value" label="操作" header-align="center" width="80">
                                    <template slot-scope="scope">
                                        <el-button type="danger" icon="el-icon-delete" size="mini"
                                                   @click.native="delTableRow('globalVar',scope.$index)">
                                        </el-button>
                                    </template>
                                </el-table-column>
                            </el-table>
                        </el-tab-pane>
                        <el-tab-pane label="参数化" name="second">
                            <el-table :data="apiMsgData.parameterized" size="mini" stripe :show-header="false"
                                      class="h-b-e-a-style"
                                      :row-style="{'background-color': 'rgb(250, 250, 250)'}">
                                <el-table-column property="key" label="Key" header-align="center" minWidth="100">
                                    <template slot-scope="scope">
                                        <el-input v-model="scope.row.key" size="mini"
                                                  placeholder="key 或者 key1-key2-key3">
                                        </el-input>
                                    </template>
                                </el-table-column>

                                <el-table-column property="value" label="Value" header-align="center" minWidth="200">
                                    <template slot-scope="scope">
                                        <el-input v-model="scope.row.value" size="mini"
                                                  placeholder='["value1", "value2] 或者 [["v1", "v2", "v3"],["v11","v22", "v33"]] 或者 ${函数名(参数, 参数, ...)}'>
                                        </el-input>
                                    </template>
                                </el-table-column>
                                <el-table-column property="value" label="操作" header-align="center" width="80">
                                    <template slot-scope="scope">
                                        <el-button type="danger" icon="el-icon-delete" size="mini"
                                                   @click.native="delTableRow('parameterized',scope.$index)">
                                        </el-button>
                                    </template>
                                </el-table-column>
                            </el-table>
                        </el-tab-pane>
                        <el-tab-pane label="setup_hooks" name="third">
                            <el-table :data="apiMsgData.setupHooks" size="mini" stripe :show-header="false"
                                      class="h-b-e-a-style"
                                      :row-style="{'background-color': 'rgb(250, 250, 250)'}">
                                <el-table-column property="key" label="Key" header-align="center" minWidth="100">
                                    <template slot-scope="scope">
                                        <el-input v-model="scope.row.key" size="mini" placeholder="key">
                                        </el-input>
                                    </template>
                                </el-table-column>
                                <el-table-column property="value" label="操作" header-align="center" width="80">
                                    <template slot-scope="scope">
                                        <el-button type="danger" icon="el-icon-delete" size="mini"
                                                   @click.native="delTableRow('setupHooks',scope.$index)">
                                        </el-button>
                                    </template>
                                </el-table-column>
                            </el-table>
                        </el-tab-pane>
                        <el-tab-pane label="teardown_hooks" name="fourth">
                            <el-table :data="apiMsgData.teardownHooks" size="mini" stripe :show-header="false"
                                      class="h-b-e-a-style"
                                      :row-style="{'background-color': 'rgb(250, 250, 250)'}">
                                <el-table-column property="key" label="Key" header-align="center" minWidth="100">
                                    <template slot-scope="scope">
                                        <el-input v-model="scope.row.key" size="mini" placeholder="key">
                                        </el-input>
                                    </template>
                                </el-table-column>
                                <el-table-column property="value" label="操作" header-align="center" width="80">
                                    <template slot-scope="scope">
                                        <el-button type="danger" icon="el-icon-delete" size="mini"
                                                   @click.native="delTableRow('teardownHooks',scope.$index)">
                                        </el-button>
                                    </template>
                                </el-table-column>
                            </el-table>
                        </el-tab-pane>

                        <el-tab-pane label="skip" name="fifth">
                            <el-table :data="apiMsgData.is_skip" size="mini" stripe :show-header="false"
                                      class="h-b-e-a-style"
                                      :row-style="{'background-color': 'rgb(250, 250, 250)'}">
                                <el-table-column property="key"  width="250px"  header-align="center" minWidth="100">
                                    <template slot-scope="scope">
                                    <el-select  v-model="scope.row.key" placeholder="是否跳过" clearable>
                                        <el-option label="直接跳过" value="skip"></el-option>
                                        <el-option label="条件成立时跳过" value="skipIf"></el-option>
                                        <el-option label="条件不成立时跳过" value="skipUnless"></el-option>
                                    </el-select>
                                    </template>
                                </el-table-column>

                                <el-table-column property="value" width="250px" minWidth="100">
                                    <template slot-scope="scope">
                                    <el-input v-model="scope.row.value" placeholder="条件"></el-input>
                                    </template>
                                </el-table-column>

                            </el-table>
                        </el-tab-pane>
                    </el-tabs>

                </el-tab-pane>
            </el-tabs>


            <el-row>
                <el-col :span="2">
                <el-button type="warning"  @click="onDebug()">调试</el-button>
                </el-col>
                <el-col :span="2">
                    <el-button type="primary" @click="onSubmit()">提交</el-button>
                </el-col>
                <el-col :span="2">
                    <el-button @click="close_page()">取消</el-button>
                </el-col>
            </el-row>
                <template v-if="showDebug">
      <hr style="margin: 10px 0;" />
      <div style="margin-bottom: 10px;">
        <el-button type="info" @click="clearDebug">清空结果</el-button>
        <!-- 提取按钮只针对最后一个响应页有效 -->
        <el-button type="primary" @click="getSelectedExtract">提取数据</el-button>
        <el-button type="primary" @click="getSelectedAssert">提取断言</el-button>
      </div>
      <el-tabs type="border-card" v-model="tabs_index" >
        <template v-for="(item, index) in treeData">
            <el-tab-pane
              :label="caseMetas[index].flag ? ('响应'+String(index+1) +':'+ caseMetas[index].name)+'(pass)' : ('响应'+String(index+1)+':' + caseMetas[index].name)+'(fail)'"
              :key="index" :name="String(index)">
              <!-- 无论对错，均显示断言信息 -->
              <template v-if="true">
                <!-- 报错的响应页，会显示当前响应的分析信息 -->
                <template v-if="!caseMetas[index].flag">
                  <el-button type="danger" @click="traceback = !traceback">Traceback</el-button>
                </template>
                <el-button type="primary" @click="validators = !validators">Validators</el-button>
                <el-row  :gutter="32">
                  <el-col :span="12">
                    <div v-if="!caseMetas[index].flag&&traceback" class="traceback">
                      <pre class="validatorPre">
                        {{caseMetas[index].attachment}}
                      </pre>
                    </div>
                  </el-col>
                  <el-col :span="12">
                    <div v-if="validators" class="validators">
                      <el-collapse style="border: none;">
                        <template v-for="(validator, vindex) in caseMetas[index].validators">
                          <span :name="String(vindex)" :key="vindex" :style="{background: validator.check_result === 'pass' ? 'green' : 'red'}">
                            {{`第${vindex+1}项 -- ${validator.check}`}}
                            <pre slot="content" :key="vindex" class="validatorPre">
                            {{`【变量】:${validator.check}
                            【检查内容】:${validator.expect}(期望值|${typeof validator.expect}) ${validator.comparator} ${validator.check_value}(实际值|${typeof validator.check_value})
                            【检查结果】:${validator.check_result}`}}
                            </pre>
                          </span >
                        </template>
                      </el-collapse>
                    </div>
                  </el-col>
                </el-row>
              </template>
              <el-tree :data="item"  :props="defaultProps" :show-checkbox="caseMetas[index].name === '当前用例'" ref="tree"></el-tree>
            </el-tab-pane>
        </template>
      </el-tabs>
    </template>
    <div class="position-box"></div>
        </div>


        <!-- 切换项目提示框 -->
        <el-dialog title="是否切换项目" :visible.sync="switchVisible" width="300px" center>
            <div class="del-dialog-cnt">切换项目将清空前置用例，是否确定切换？</div>
            <span slot="footer" class="dialog-footer">
                <el-button @click="changeProjectCancle">取 消</el-button>
                <el-button type="primary" @click="getModulesByProjectID(selected_project_id)">确 定</el-button>
            </span>
        </el-dialog>

        <!-- 编辑弹出框 -->
        <el-dialog title="编辑用例" :visible.sync="editVisible" width="28%" center>
            <el-form label-width="120px">
                <el-form-item label="用例名称" required>
                    <el-input v-model="testcase_name" clearable></el-input>
                </el-form-item>

                <el-form-item label="测试人员" required>
                    <el-input v-model="author" clearable></el-input>
                </el-form-item>

                <el-form-item label="选择项目" required>
                    <el-select v-model="selected_project_id" placeholder="请选择"
                               @change="getModulesByProjectID(selected_project_id)" disabled>
                        <el-option v-for="(item, key) in project_names" :key="key"
                                   :label="item.name" :value="item.id">
                        </el-option>
                    </el-select>
                </el-form-item>

                <el-form-item label="选择模块" required>
                    <el-select v-model="selected_module_id" placeholder="请选择">
                        <el-option v-for="(item, key) in modules" :key="key" :label="item.name"
                                   :value="item.id">
                        </el-option>
                    </el-select>
                </el-form-item> 

            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveEdit">确 定</el-button>
            </span>
        </el-dialog>

        <!-- 调试弹框 -->
        <el-dialog title="调试" :visible.sync="debugVisible" width="30%" center>
            <el-form  label-width="120px">
                <el-form-item label="运行环境">
                    <el-select v-model="env_id" clearable placeholder="请选择">
                        <el-option
                            v-for="item in envs_id_names"
                            :key="item.id"
                            :label="item.name"
                            :value="item.id"
                        ></el-option>
                    </el-select>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="debugVisible = false">取 消</el-button>
                <el-button type="primary" @click="debugRun">运行</el-button>
            </span>
        </el-dialog>

    </div>
</template>

<script>
    import draggable from 'vuedraggable';
    import bus from '../common/bus';
    import {
        add_testcase,
        projects_names,
        modules_by_project_id,
        configures_all,
        testcases_by_module_id,
        get_detail_testcase,
        get_detail_configure,
        envs_names,
        debug,
        upload_file,       
    } from '../../api/api';
    import host from '../../api/api';

    export default {
        name: 'baseform',
        data: function () {
            return {
                uploadUrl:'',
                current_testcase_id: null,
                switchVisible:false,
                editVisible: false,   // 新增项目弹框是否显示标识
                methods: ['POST', 'GET', 'PUT', 'DELETE'],  // 请求方法
                types: ['data', 'json', 'params'],  // 请求类型
                ParamViewStatus: false,             // params按钮状态
                comparators: [{'value': 'equals'}, {'value': 'contains'}, {'value': 'contained_by'},
                    {'value': 'startswith'}, {'value': 'endswith'}, {'value': 'regex_match'},
                    {'value': 'less_than'}, {'value': 'less_than_or_equals'},
                    {'value': 'greater_than'}, {'value': 'greater_than_or_equals'}, {'value': 'not_equals'},
                    {'value': 'string_equals'}, {'value': 'length_equals'}, {'value': 'length_greater_than'},
                    {'value': 'count_greater_than_or_equals'}, {'value': 'length_less_than'},
                    {'value': 'length_less_than_or_equals'}],
                apiMsgData: {
                    id: null,
                    method: 'POST',
                    name: "",
                    url: '',
                    choiceType: 'json',
                    param: [{key: null, value: null}],
                    header: [{key: null, value: null}],
                    variable: [{key: null, value: null, param_type: 'string'}],
                    filesVariable: [],
                    jsonVariable: '',
                    extract: [{key: null, value: null}],
                    validate: [{key: null, value: null, comparator: 'equals', param_type: 'string'}],
                    globalVar: [{key: null, value: null, param_type: 'string'}],
                    parameterized: [{key: null, value: null}],
                    setupHooks: [{key: null}],
                    teardownHooks: [{key: null}],
                    is_skip:[{key: null, value: null}],
                },
                bodyShow: 'second',
                otherShow: 'first',
                paramTypes: ['string', 'int', 'float', 'boolean'],
                cell: Object(),
                dragOptions: {
                    animation: 120,
                    scroll: true,
                    group: 'sortlist',
                    ghostClass: 'ghost-style'
                },
                project_names: [],
                choose_selected_module_id: null,
                selected_project_id: null,
                before_selected_project_id:null,
                selected_module_id: null,
                selected_configure_id: null,
                selected_testcase: [],   // 已选择的用例
                selected_testcase_id:[],
                selected_testcase_after: [],
                selected_testcase_after_id: [],
                testcase_name: null,  // 用例名称
                author: '',     // 用例编写人员
                modules: [],
                choose_modules: [],
                configures: [],
                unselected: [],     // 未选择的用例
                configure_globalVar:[],
                configure_header:[],
                env_id:'',
                envs_id_names:[],
                debugVisible:false,
                showDebug: false,
                treeData: [],
                caseMetas: [],
                treeDataBackup: [],
                caseMetasBackup: [],
                traceback: false,
                validators: false,
                defaultProps: {
                children: 'children',
                label: 'title'
                },
                is_scroll:false,
                tabs_index:0,
                                           }
        },
      
        created() {
            this.getProjectNames();
            this.getConf();
            this.getEnvsIdNames();
            this.uploadUrl = host +"/testcases/upload_file/"  ;
        },
        components: {
            draggable,
            editor: require('vue2-ace-editor'),
        },
        methods: {
        handleChange(file, fileList) {
            this.apiMsgData.filesVariable = fileList;
        }, 
            handleRemove(file, fileList) {
            this.apiMsgData.filesVariable = fileList;
        },
            close_page(){
                this.$router.go(-1);
                bus.$emit("close_current_tags");
                
            },
            getEnvsIdNames() {
                envs_names()
                    .then((response) => {
                        this.envs_id_names = response.data; // 将返回的环境变量数据赋值给envs_id_names
                    })
                    .catch((error) => {
                        this.$message.error('服务器错误');
                    });
            },
            changeProjectCancle(){
                this.selected_project_id = this.before_selected_project_id;
                this. switchVisible = false;

            },
            getConfigureDetail(selected_configure_id){
                if(this.configure_globalVar){
                    this.configure_globalVar.forEach(element =>{
                        this.apiMsgData.globalVar = this.apiMsgData.globalVar.filter((item) =>{
                            return item.key !== element.key;
                        })
                    })

                };
                if(this.configure_header){
                    this.configure_header.forEach(element =>{
                        this.apiMsgData.header = this.apiMsgData.header.filter((item) =>{
                            return item.key !== element.key;
                        })
                    })

                }
                if(selected_configure_id){
                    get_detail_configure(selected_configure_id)
                    .then(response => {
                        this.apiMsgData.globalVar = this.apiMsgData.globalVar.filter((item) =>{
                            return item.key !== null;
                        })
                        response.data.globalVar.forEach(element =>{
                            this.apiMsgData.globalVar.push(element)
                        });
                        this.apiMsgData.header = this.apiMsgData.header.filter((item) =>{
                            return item.key !== null;
                        })
                        response.data.header.forEach(element =>{
                            this.apiMsgData.header.push(element)
                        });
                        this.configure_globalVar = response.data.globalVar;
                        this.configure_header = response.data.header;
                        
                    })
                    .catch(error => {
                        this.$message.error('服务器错误');
                    })

                };
            },
            getConfigureFirstDetail(selected_configure_id){
                if(selected_configure_id){
                    get_detail_configure(selected_configure_id)
                    .then(response => {
                        this.configure_globalVar = response.data.globalVar;
                        this.configure_header = response.data.header;
                        ;
                        
                    })
                    .catch(error => {
                        this.$message.error('服务器错误');
                    })

                };

                
            },
            editorInit() {
                require('brace/ext/language_tools');
                require('brace/mode/json');
                require('brace/theme/chrome');
                require('brace/snippets/json')
            },
            onSubmit() {
                if(this.apiMsgData.is_skip[0].key == "skip"){
                    if(!this.apiMsgData.is_skip[0].value){
                        this.$message.error('请输入跳过原因');
                        return
                    }
                }else if(this.apiMsgData.is_skip[0].key == "skipIf" ||this.apiMsgData.is_skip[0].key == "skipUnless"){

                        if(!this.apiMsgData.is_skip[0].value){
                            this.$message.error('请输入跳过条件');
                            return
                        }
                }

                if (this.apiMsgData.url.length === 0){
                    this.$message.error('没有输入请求URL');
                    return
                }

                let validate = this.apiMsgData.validate;
                validate.splice(-1, 1);
                if (validate.length === 0) {
                    this.$message.error('未设置Assert断言!');
                    return
                }
                if(this.selected_project_id){
                    this.hava_project=true
                }

                this.editVisible = true;
            },
            switchProject(){
                if(this.selected_testcase.length != 0 || this.selected_testcase_after.length){
                    this.switchVisible = true;
                }
                else{
                    this.getModulesByProjectID(this.selected_project_id);
                }
                

            },
            onDebug() {
                if (this.apiMsgData.url.length === 0){
                    this.$message.error('没有输入请求URL');
                    return
                }
                if (this.selected_project_id === null || this.choose_selected_module_id === null){
                    this.$message.error('未选择所属项目或者模块!');
                    return
                }
                this.debugVisible = true;
            },
            
            // 处理数据1, 有param_type, 返回js对象
            handleData1(request_data, msg){
                let one_data = {};
                for(let i = 0; i < request_data.length; i++) {
                    let key = request_data[i].key;
                    if (! key) {
                        this.$message.error(msg + '的key为空!');
                        return []
                    }
                    let param_type = request_data[i].param_type;
                    let value = request_data[i].value;
                    if (param_type === 'int') {
                        if (/^\d+$/.test(value)) {
                            value = Number(value);
                        } else {
                            this.$message.error(msg + '不是整数int类型!');
                            return []
                        }
                    } else if (param_type === 'float') {
                        if (/^[+-]?\d+(\.\d+)?$/.test(value)) {
                            value = Number(value);
                        } else {
                            this.$message.error(msg + '不是小数float类型!');
                            return []
                        }
                    } else if (param_type === 'boolean') {
                        if (/^(true|True|TRUE|1|0)$/.test(value)) {
                            value = true;
                        } else if (/^(false|False|FALSE|0)$/.test(value)) {
                            value = false;
                        } else {
                            this.$message.error(msg + '不是布尔boolean类型!');
                            return []
                        }
                    }
                    one_data[key] = value;
                }

                return one_data
            },

            // 处理数据11, 有param_type, 返回js数组
            handleData11(request_data, msg){
                let data_arr = [];
                for(let i = 0; i < request_data.length; i++) {
                    let key = request_data[i].key;
                    if (! key) {
                        this.$message.error(msg + '的key为空!');
                        return []
                    }
                    let param_type = request_data[i].param_type;
                    let value = request_data[i].value;
                    if (param_type === 'int') {
                        if (/^\d+$/.test(value)) {
                            value = Number(value);
                        } else {
                            this.$message.error(msg + '不是整数int类型!');
                            return []
                        }
                    } else if (param_type === 'float') {
                        if (/^[+-]?\d+(\.\d+)?$/.test(value)) {
                            value = Number(value);
                        } else {
                            this.$message.error(msg + '不是小数float类型!');
                            return []
                        }
                    } else if (param_type === 'boolean') {
                        if (/^(true|True|TRUE|1|0)$/.test(value)) {
                            value = true;
                        } else if (/^(false|False|FALSE|0)$/.test(value)) {
                            value = false;
                        } else {
                            this.$message.error(msg + '不是布尔boolean类型!');
                            return []
                        }
                    }
                    let one_data = {};
                    one_data[key] = value;
                    data_arr.push(one_data)
                }

                return data_arr
            },

            // 处理数据2, 无param_type, 返回js对象
            handleData2(request_data, msg){
                let one_data = {};
                for(let i = 0; i < request_data.length; i++) {
                    let key = request_data[i].key;
                    if (! key) {
                        this.$message.error(msg + '的key为空!');
                        return []
                    }
                    one_data[key] = request_data[i].value;
                }
                return one_data
            },

            // 处理数据22, 无param_type, 专门处理参数化、extract, 返回js数组
            handleData22(request_data, msg){
                let data_arr = [];
                for(let i = 0; i < request_data.length; i++) {
                    let key = request_data[i].key;
                    if (key==null) {
                        this.$message.error(msg + '的key为空!');
                        return []
                    }
                    let value = request_data[i].value;
                    let one_data = {};
                    //如果参数化值是列表的形式(不是函数也不是csv), 将列表转化为json数组
                    if (/^\[/.test(value)) {
                        value = JSON.parse(value);
                    }
                    one_data[key] = value;
                    data_arr.push(one_data)
                }
                return data_arr
            },

            // 处理数据3, 无value, 返回js数组
            handleData3(request_data, msg){
                let data_arr = [];
                for(let i = 0; i < request_data.length; i++) {
                    let key = request_data[i].key;
                    if (! key) {
                        this.$message.error(msg + '的key为空!');
                        return []
                    }
                    data_arr.push(key)
                }
                return data_arr
            },

            // 处理数据4, validate数据处理, 返回js数组
            handleData4(request_data, msg){
                let data_arr = [];
                for(let i = 0; i < request_data.length; i++) {
                    let key = request_data[i].key;
                    // console.log('key: ', key);
                    if (! key) {
                        this.$message.error(msg + '的key为空!');
                        return []
                    }
                    let param_type = request_data[i].param_type;
                    let value = request_data[i].value;
                    let comparator = request_data[i].comparator;

                    if (param_type === 'int') {
                        if (/^\d+$/.test(value)) {
                            value = Number(value);
                        } else {
                            this.$message.error(msg + '不是整数int类型!');
                            return []
                        }
                    } else if (param_type === 'float') {
                        if (/^[+-]?\d+(\.\d+)?$/.test(value)) {
                            value = Number(value);
                        } else {
                            this.$message.error(msg + '不是小数float类型!');
                            return []
                        }
                    } else if (param_type === 'boolean') {
                        if (/^(true|True|TRUE|1|0)$/.test(value)) {
                            value = true;
                        } else if (/^(false|False|FALSE|0)$/.test(value)) {
                            value = false;
                        } else {
                            this.$message.error(msg + '不是布尔boolean类型!');
                            return []
                        }
                    }
                    let one_data = {};
                    one_data['check'] = key;
                    one_data['expected'] = value;
                    one_data['comparator'] = comparator;
                    data_arr.push(one_data)
                }

                return data_arr
            },

            // 保存编辑
            saveEdit() {
                this.changeResult();
                this.changeResultAfter();
                if (this.testcase_name === null){
                    this.$message.error('用例名称不能为空!');
                    return
                }

                if (this.author === ''){
                    this.$message.error('测试人员名称不能为空!');
                    return
                }

                if (this.selected_project_id === null || this.selected_module_id === null){
                    this.$message.error('未选择所属项目或者模块!');
                    return
                }

                if (this.selected_configure_id === '') {
                    this.selected_configure_id = null;
                }
                let include = {"config": this.selected_configure_id, "testcases": this.selected_testcase_id,"testcases_after":this.selected_testcase_after_id};

                let handle_url = this.apiMsgData.url.trim().split('?', 1)[0];   // 去掉前后空格之后, 以问号进行切割, 取第一部分
                let datas={}
                if (this.apiMsgData.is_skip[0].key){
                    datas = {
                    "name": this.testcase_name,           // 用例名称
                    "include": include,       // 用例执行前置顺序
                    "module": {
                        "pid": this.selected_project_id,      // 项目ID
                        "iid": this.selected_module_id,      // 模块ID
                    },
                    "author": this.author,         // 用例编写人员
                    "request": {          // 请求信息
                        "test": {
                            "name": this.testcase_name,
                            [this.apiMsgData.is_skip[0].key]:this.apiMsgData.is_skip[0].value,
                            "request": {
                                "url": handle_url,
                                "method": this.apiMsgData.method,
                                
                            },
                        }
                    },
                    "files":JSON.stringify(this.apiMsgData.filesVariable),
                };

                }else{
                    datas = {
                    "name": this.testcase_name,           // 用例名称
                    "include": include,       // 用例执行前置顺序
                    "module": {
                        "pid": this.selected_project_id,      // 项目ID
                        "iid": this.selected_module_id,      // 模块ID
                    },
                    "author": this.author,         // 用例编写人员
                    "request": {          // 请求信息
                        "test": {
                            "name": this.testcase_name,
                            "request": {
                                "url": handle_url,
                                "method": this.apiMsgData.method,
                                
                            },
                            
                        }
                    },
                    "files":JSON.stringify(this.apiMsgData.filesVariable),
                };};

                // 处理查询字符串参数
                let params_data = this.apiMsgData.param;
                params_data.splice(-1, 1);   // 删除最后一个空元素
                if (params_data.length !== 0) {
                    let new_data = this.handleData2(params_data, 'param参数');
                    if (new_data.length === 0) {
                        return
                    }
                    datas.request.test.request['params'] = new_data
                }

                let paramsType = '';
                let request_data = {};
                let globalVar = []
                if (this.apiMsgData.choiceType === 'files') {
                    globalVar = this.apiMsgData.globalVar.filter((item) =>{
                            return item.key !== null;
                        })
                    paramsType = 'files';
                    let len = this.apiMsgData.filesVariable.length
                    for (let i = 0; i < len; i++){
                        let fileKey = "filepath"+(i+1);
                        let fileValue = this.apiMsgData.filesVariable[i].response["files_list"][0]
                        globalVar.push(
                            {
                                key:fileKey,
                                value:fileValue,
                                param_type:'file'
                            }
                        )

                        request_data["file"+(i+1)]=[this.apiMsgData.filesVariable[i].name,"${get_file($"+fileKey+")}"]
                        

                    }
              
               
                    datas.request.test.request['files'] = request_data

                }
                else if (this.apiMsgData.choiceType === 'json'){
                    paramsType = 'json';
                    request_data = this.apiMsgData.jsonVariable;
                    if (request_data.length !== 0) {
                        datas.request.test.request['json'] = JSON.parse(request_data)
                    }
                }else {
                    paramsType = 'data';
                    request_data = this.apiMsgData.variable;
                    request_data.splice(-1, 1);
                    if (request_data.length !== 0) {
                        let new_data = this.handleData1(request_data, 'form-data参数');
                        if (new_data.length === 0) {
                            return
                        }
                        datas.request.test.request['data'] = new_data
                    }
                }

                // 参数化
                let parameterized = this.apiMsgData.parameterized;
                parameterized.splice(-1, 1);
                if (parameterized.length !== 0) {
                    let new_data = this.handleData22(parameterized, '参数化参数');
                    if (new_data.length === 0) {
                        return
                    }
                    datas.request.test['parameters'] = new_data;
                }

                // variables处理
                let variables = globalVar.length > 0 ? globalVar:this.apiMsgData.globalVar;
                if(!variables[variables.length-1]["key"]){
                    variables.splice(-1, 1);
                }

                if (variables.length !== 0) {
                    let new_data = this.handleData11(variables, '全局变量variables');
                    if (new_data.length === 0) {
                        return
                    }
                    datas.request.test['variables'] = new_data;
                }

                // headers处理
                let headers = this.apiMsgData.header;
                headers.splice(-1, 1);
                if (headers.length !== 0) {
                    let new_data = this.handleData2(headers, '请求头header');
                    if (new_data.length === 0) {
                        return
                    }
                    datas.request.test.request['headers'] = new_data;
                }

                // extract处理
                let extract = this.apiMsgData.extract;
                extract.splice(-1, 1);
                if (extract.length !== 0) {
                    let new_data = this.handleData22(extract, 'extract参数');
                    if (new_data.length === 0) {
                        return
                    }
                    datas.request.test['extract'] = new_data;
                }

                // validate处理
                let validate = this.apiMsgData.validate;
                validate.splice(-1, 1);
                if (validate.length !== 0) {
                    let new_data = this.handleData4(validate, 'Assert断言参数');
                    if (new_data.length === 0) {
                        return
                    }
                    datas.request.test['validate'] = new_data;
                } else {
                    this.$message.error('未设置Assert断言!');
                    return
                }

                // setup_hooks处理
                let setup_hooks = this.apiMsgData.setupHooks;
                setup_hooks.splice(-1, 1);
                if (setup_hooks.length !== 0) {
                    let new_data = this.handleData3(setup_hooks, '请求钩子setup_hooks');
                    if (new_data.length === 0) {
                        return
                    }
                    datas.request.test['setup_hooks'] = new_data;
                }

                // teardown_hooks处理
                let teardown_hooks = this.apiMsgData.teardownHooks;
                teardown_hooks.splice(-1, 1);
                if (teardown_hooks.length !== 0) {
                    let new_data = this.handleData3(teardown_hooks, '请求钩子teardown_hooks');
                    if (new_data.length === 0) {
                        return
                    }
                    datas.request.test['teardown_hooks'] = new_data;
                }

                datas.include = JSON.stringify(datas.include);
                datas.request = JSON.stringify(datas.request);
                add_testcase(datas)
                    .then(response => {
                        this.editVisible = false;
                        this.$message.success(`新增用例成功`);
                        // 1秒钟之后, 执行刷新
                        this.close_page();

                    })
                    .catch(error => {
                        this.editVisible = false;
                        if (typeof error === 'object' && error.hasOwnProperty('name')) {
                            console.log(error);
                            this.$message.error(error.name[0]);
                        } else {
                            console.log(error);
                            this.$message.error('服务器错误');
                        }
                    })

            },

            debugRun() {
                if(!this.env_id){
                    this.$message.error('请选择运行环境!');
                    return
                }
                this.changeResult();
                this.changeResultAfter();

                let include = {"config": this.selected_configure_id, "testcases": this.selected_testcase_id,"testcases_after":this.selected_testcase_after_id};

                let handle_url = this.apiMsgData.url.trim().split('?', 1)[0];   // 去掉前后空格之后, 以问号进行切割, 取第一部分
                let datas = {
                    "name": "当前用例",           // 用例名称
                    "include": include,       // 用例执行前置顺序
                    "module": {
                        "pid": this.selected_project_id,      // 项目ID
                        "iid": this.choose_selected_module_id,      // 模块ID
                    },
                    "author": "无",         // 用例编写人员
                    "request": {          // 请求信息
                        "test": {
                            "name": "当前用例",
                            "request": {
                                "url": handle_url,
                                "method": this.apiMsgData.method,
                            }
                            
                        }
                    },
                };

                // 处理查询字符串参数
                let params_data = this.apiMsgData.param;
                params_data.splice(-1, 1);   // 删除最后一个空元素
                if (params_data.length !== 0) {
                    let new_data = this.handleData2(params_data, 'param参数');
                    if (new_data.length === 0) {
                        return
                    }
                    datas.request.test.request['params'] = new_data
                }

                let paramsType = '';
                let request_data = {};
                let globalVar = []
                if (this.apiMsgData.choiceType === 'files') {
                    globalVar = this.apiMsgData.globalVar.filter((item) =>{
                            return item.key !== null;
                        })
                    paramsType = 'files';
                    let len = this.apiMsgData.filesVariable.length
                    for (let i = 0; i < len; i++){
                        let fileKey = "filepath"+(i+1);
                        let fileValue = this.apiMsgData.filesVariable[i].response["files_list"][0]
                        globalVar.push(
                            {
                                key:fileKey,
                                value:fileValue,
                                param_type:'file'
                            }
                        )

                        request_data["file"+(i+1)]=[this.apiMsgData.filesVariable[i].name,"${get_file($"+fileKey+")}"]
                        

                    }
              
               
                    datas.request.test.request['files'] = request_data

                }
                else if (this.apiMsgData.choiceType === 'json'){
                    paramsType = 'json';
                    request_data = this.apiMsgData.jsonVariable;
                    if (request_data.length !== 0) {
                        datas.request.test.request['json'] = JSON.parse(request_data)
                    }
                }else {
                    paramsType = 'data';
                    request_data = this.apiMsgData.variable;
                    request_data.splice(-1, 1);
                    if (request_data.length !== 0) {
                        let new_data = this.handleData1(request_data, 'form-data参数');
                        if (new_data.length === 0) {
                            return
                        }
                        datas.request.test.request['data'] = new_data
                    }
                }

                // 参数化
                let parameterized = this.apiMsgData.parameterized;
                parameterized.splice(-1, 1);
                if (parameterized.length !== 0) {
                    let new_data = this.handleData22(parameterized, '参数化参数');
                    if (new_data.length === 0) {
                        return
                    }
                    datas.request.test['parameters'] = new_data;
                }

                // variables处理
                let variables = globalVar.length > 0 ? globalVar:this.apiMsgData.globalVar;
                if(!variables[variables.length-1]["key"]){
                    variables.splice(-1, 1);
                }
                if (variables.length !== 0) {
                    let new_data = this.handleData11(variables, '全局变量variables');
                    if (new_data.length === 0) {
                        return
                    }
                    datas.request.test['variables'] = new_data;
                }

                // headers处理
                let headers = this.apiMsgData.header;
                headers.splice(-1, 1);
                if (headers.length !== 0) {
                    let new_data = this.handleData2(headers, '请求头header');
                    if (new_data.length === 0) {
                        return
                    }
                    datas.request.test.request['headers'] = new_data;
                }

                // extract处理
                let extract = this.apiMsgData.extract;
                extract.splice(-1, 1);
                if (extract.length !== 0) {
                    let new_data = this.handleData22(extract, 'extract参数');
                    if (new_data.length === 0) {
                        return
                    }
                    datas.request.test['extract'] = new_data;
                }

                // validate处理
                let validate = this.apiMsgData.validate;
                validate.splice(-1, 1);
                if (validate.length !== 0) {
                    let new_data = this.handleData4(validate, 'Assert断言参数');
                    if (new_data.length === 0) {
                        return
                    }
                    datas.request.test['validate'] = new_data;
                } 

                // setup_hooks处理
                let setup_hooks = this.apiMsgData.setupHooks;
                setup_hooks.splice(-1, 1);
                if (setup_hooks.length !== 0) {
                    let new_data = this.handleData3(setup_hooks, '请求钩子setup_hooks');
                    if (new_data.length === 0) {
                        return
                    }
                    datas.request.test['setup_hooks'] = new_data;
                }

                // teardown_hooks处理
                let teardown_hooks = this.apiMsgData.teardownHooks;
                teardown_hooks.splice(-1, 1);
                if (teardown_hooks.length !== 0) {
                    let new_data = this.handleData3(teardown_hooks, '请求钩子teardown_hooks');
                    if (new_data.length === 0) {
                        return
                    }
                    datas.request.test['teardown_hooks'] = new_data;
                }

                datas.include = JSON.stringify(datas.include);
                datas.request = JSON.stringify(datas.request);
                datas.env_id = this.env_id
                debug(datas)
                    .then(response => {
                        this.showDebug = true;
                        this.$message.success(`调试成功`);
                        this.treeData = response.data.tree;
                        this.treeDataBackup = response.data.tree;
                        this.caseMetas = response.data.case_metas;
                        this.caseMetasBackup = response.data.case_metas;
                        this.tabs_index = String(this.treeData.length-1);
                        this.debugVisible = false;
                        this.$nextTick(function () {
                            document.getElementsByClassName('position-box')[0].scrollIntoView();
                        })

                    })
                    .catch(error => {
                        if (typeof error === 'object' && error.hasOwnProperty('name')) {
                            console.log(error);
                            this.$message.error(error.name[0]);
                        } else {
                            console.log(error);
                            this.$message.error('服务器错误');
                        }
                    })

            },
            clearDebug() {
                // 关闭错误信息显示
                this.traceback = false
                this.validators = false
                // 清空已有的调试结果
                this.showDebug = false
            },
            rightLabel(index, reqName) {
                return (h) => {
                    return h('div', {style: {color: 'green'}}, [ // '#19be6b'
                    h('Icon', {
                        props: {
                        type: 'md-checkmark-circle'
                        }
                    }),
                    h('span', `响应${index}:` + reqName)
                    ])
                }
            },
            wrongLabel(index, reqName) {
                return (h) => {
                    return h('div', {style: {color: 'red'}}, [ // '#ed4014'
                    h('Icon', {
                        props: {
                        type: 'md-close-circle'
                        }
                    }),
                    h('span', `响应${index}:` + reqName)
                    ])
                }
            },
            getSelectedAssert() {
            // 只取当前的请求结果
            this.apiMsgData.validate = this.apiMsgData.validate.filter((item) =>{
                return item.key !== null;
            })
            let treeEle = this.$refs.tree[this.tabs_index]
            let checkedNodes = treeEle.getCheckedNodes()
            // 只取末节点
            checkedNodes = checkedNodes.filter(item => {
                return String(item.children) === 'undefined'
            })
            if (checkedNodes.length === 0) {
                this.$message.warning('请先勾  选需要提取的数据')
                return
            }
            for (let i = 0; i < checkedNodes.length; i++) {
                let is_push = true;
                let validateType = null;
                let expected = checkedNodes[i].expect;
                if (typeof expected === 'number') {
                validateType = expected.toString().indexOf('.') > -1 ? 'float' : 'int'
                } else if (typeof expected === 'object') {
                // 平台未支持对象类型数据的校验，所以此处转成字串类型，但是对象类型的比较会失败
                validateType = 'string'
                expected = JSON.stringify(expected)
                } else {                  
                validateType = typeof expected
                expected = String(expected)
                };
                this.apiMsgData.validate.forEach((item,index,arr)=>{
                    if(item.key ==checkedNodes[i].path.trim() ){
                        this.apiMsgData.validate[index].value=expected;
                        this.apiMsgData.validate[index].param_type=validateType
                        is_push = false
                    }}
                );
                if(is_push){
                this.apiMsgData.validate.push({
                key: checkedNodes[i].path.trim(),
                value: expected,
                comparator: "equals",
                param_type: validateType,
                }  
                )};
            }

            },
            getSelectedExtract() {              
                this.apiMsgData.extract = this.apiMsgData.extract.filter((item) =>{
                    return item.key !== null;
                })
                let treeEle = this.$refs.tree[this.tabs_index]
                let checkedNodes = treeEle.getCheckedNodes()
                // 只取末节点
                checkedNodes = checkedNodes.filter(item => {
                    return String(item.children) === 'undefined'
                })
                if (checkedNodes.length === 0) {
                    this.$message.warning('请先勾  选需要提取的数据')
                    return
                }
                for (let i = 0; i < checkedNodes.length; i++) {
                    let is_push = true
                    this.apiMsgData.extract.forEach((item,index,arr)=>{
                        if(item.key ==checkedNodes[i].name ){
                            this.apiMsgData.extract[index].value=checkedNodes[i].path.trim();
                            is_push = false
                        }}
                    );
                    if(is_push){
                    this.apiMsgData.extract.push({
                    key: checkedNodes[i].name,
                    value: checkedNodes[i].path.trim(),
                    }  
                    )}
                
                }

            },
            getProjectNames() {
                projects_names()
                    .then((response) => {
                        this.project_names = response.data;
                    })
                    .catch(error => {
                        that.$message.error('服务器错误');
                    });
            },
            getChooseModulesByProjectID(pro_id) {
                modules_by_project_id(pro_id)
                    .then((response) => {
                        this.choose_modules = response.data;
                        if (response.data.length != 0){
                            this.choose_selected_module_id = response.data[0].id;
                            this.getTestcaseByModuleID(this.choose_selected_module_id);
                        } else {
                            this.choose_selected_module_id = null;
                            this.unselected= null;

                        }
                    })
                    .catch(error => {
                        that.$message.error('服务器错误');
                    });

            },
            //初始化时，获取前置用例可选择的模块
            getCModulesByProjectID(pro_id) {
                modules_by_project_id(pro_id)
                    .then((response) => {
                        this.choose_modules = response.data;
                    })
                    .catch(error => {
                        that.$message.error('服务器错误');
                    });
            },
            //初始化时，获取当前用例所属模块
            getModules(pro_id) {
                modules_by_project_id(pro_id)
                    .then((response) => {
                        this.modules = response.data;
     
                    })
                    .catch(error => {
                        that.$message.error('服务器错误');
                    });           
            },
            
            getModulesByProjectID(pro_id) {
                this.before_selected_project_id = pro_id;
                modules_by_project_id(pro_id)
                    .then((response) => {
                        this.choose_modules = response.data;
                        this.modules = response.data;
                        if (response.data.length != 0){
                            this.choose_selected_module_id = response.data[0].id;
                            this.getTestcaseByModuleID(this.choose_selected_module_id);
                            this.selected_module_id = response.data[0].id;
                        } else {
                            this.choose_selected_module_id = null;
                            this.selected_module_id = null;
                            this.unselected= null;

                        }
                    })
                    .catch(error => {
                        that.$message.error('服务器错误');
                    }); 
                    this.switchVisible = false;
                    this.selected_testcase = [];
                    this.selected_testcase_after = [];        
            },
            getConf() {
                configures_all()
                    .then((response) => {
                        this.configures = response.data
                    })
                    .catch(error => {
                        that.$message.error('服务器错误');
                    });
            },

            getTestcaseByModuleID(choose_selected_module_id) {
                testcases_by_module_id(choose_selected_module_id)
                    .then((response) => {
                        this.unselected = response.data;
                        if (this.selected_testcase.length != 0){
                            this.selected_testcase.forEach(element => {
                            this.unselected = this.unselected.filter((item)=>{
                            return item.id !== element.id;
                             });
                        });
                        
                        }
                        if (this.selected_testcase_after.length != 0){
                            this.selected_testcase_after.forEach(element => {
                            this.unselected = this.unselected.filter((item)=>{
                            return item.id !== element.id;
                             });
                        });
                        
                        }
                        this.unselected = this.unselected.filter((item)=>{
                            return item.id != this.current_testcase_id;
                             });
                    })
                    .catch(error => {
                        that.$message.error('服务器错误');
                    });
            },
            changeResult() {
                let len = this.selected_testcase.length;
                let text = "[";
                for (let i = 0; i < len; i++) {
                    if (i === len - 1) {
                        text += this.selected_testcase[i].id + "]";
                    } else {
                        text += this.selected_testcase[i].id + ", ";
                    }

                }
                if (len === 0) {
                    text = "[]";
                }
                this.selected_testcase_id = JSON.parse(text);
            },

            changeResultAfter() {
                let len = this.selected_testcase_after.length;
                let text = "[";
                for (let i = 0; i < len; i++) {
                    if (i === len - 1) {
                        text += this.selected_testcase_after[i].id + "]";
                    } else {
                        text += this.selected_testcase_after[i].id + ", ";
                    }

                }
                if (len === 0) {
                    text = "[]";
                }
                this.selected_testcase_after_id = JSON.parse(text);
            },
            delTableRow(type, i) {
                if (type === 'variable') {
                    this.apiMsgData.variable.splice(i, 1);
                } else if (type === 'header') {
                    this.apiMsgData.header.splice(i, 1);
                } else if (type === 'validate') {
                    this.apiMsgData.validate.splice(i, 1);
                } else if (type === 'extract') {
                    this.apiMsgData.extract.splice(i, 1);
                } else if (type === 'param') {
                    this.apiMsgData.param.splice(i, 1);
                }else if (type === 'globalVar') {
                    this.apiMsgData.globalVar.splice(i, 1);
                }else if (type === 'parameterized') {
                    this.apiMsgData.parameterized.splice(i, 1);
                }else if (type === 'setupHooks') {
                    this.apiMsgData.setupHooks.splice(i, 1);
                }else if (type === 'teardownHooks') {
                    this.apiMsgData.teardownHooks.splice(i, 1);
                }
            },
            addTableRow(type) {
                if (type === 'variable') {
                    this.apiMsgData.variable.push({key: null, value: null, param_type: 'string'});
                } else if (type === 'header') {
                    this.apiMsgData.header.push({key: null, value: null});
                } else if (type === 'validate') {
                    this.apiMsgData.validate.push({key: null, value: null, comparator: 'equals', param_type: 'string'});
                } else if (type === 'extract') {
                    this.apiMsgData.extract.push({key: null, value: null});
                } else if (type === 'param') {
                    this.apiMsgData.param.push({key: null, value: null});
                } else if (type === 'globalVar') {
                    this.apiMsgData.globalVar.push({key: null, value: null, param_type: 'string'});
                } else if (type === 'parameterized') {
                    this.apiMsgData.parameterized.push({key: null, value: null});
                } else if (type === 'setupHooks') {
                    this.apiMsgData.setupHooks.push({key: null});
                } else if (type === 'teardownHooks') {
                    this.apiMsgData.teardownHooks.push({key: null});
                }
            },
            formatData() {
                // 格式化json字符串
                try {
                    this.apiMsgData.jsonVariable = JSON.parse(this.apiMsgData.jsonVariable);
                    this.apiMsgData.jsonVariable = JSON.stringify(this.apiMsgData.jsonVariable, null, 4);
                } catch (err) {
                    this.$message({
                        showClose: true,
                        message: 'json格式错误',
                        type: 'warning',
                    });
                }
            },
            tempNum(i) {
                this.temp_num = i;
            },
            resetLine() {
                //  重置单元格高度
                this.cell.style.height = '18px';
            },
            showLine(prefix, n) {
                //  获取单元格的滚动条高度，并使单元格为该高度
                this.cell = document.getElementById(prefix + n);
                this.cell.style.height = this.cell.scrollHeight + 'px';
            },
            changeLine() {
                //  当单元格高度和滚动条高度不一致时，改变单元格高度
                if (this.cell.style.height !== this.cell.scrollHeight + 'px') {
                    let i = parseInt(this.cell.style.height.substring(0, this.cell.style.height.length - 2));
                    if (i - this.cell.scrollHeight === 2) {
                        //  为true时，为减少高度操作
                        this.cell.style.height = (i - 18) + 'px'
                    }
                    else {
                        this.cell.style.height = this.cell.scrollHeight + 'px';
                    }

                }
            },
            querySearch(queryString, cb) {
                // 调用 callback 返回建议列表的数据
                cb(this.comparators);
            },
        },
        computed: {
            headers() {
                const token = sessionStorage.getItem('token') || localStorage.getItem('token');
                return{
                    "Authorization": `JWT ${token}`// 直接从本地获取token就行
                }
            },
            monitorParam() {
                return this.apiMsgData.param;
            },
            monitorUrl() {
                return this.apiMsgData.url;
            },
            monitorMethod() {
                return this.apiMsgData.method;
            },
            monitorVariable() {
                return this.apiMsgData.variable;
            },
            monitorHeader() {
                return this.apiMsgData.header;
            },
            monitorExtract() {
                return this.apiMsgData.extract;
            },
            monitorValidate() {
                return this.apiMsgData.validate;
            },

            monitorGlobalVar() {
                return this.apiMsgData.globalVar;
            },
            monitorParameterized() {
                return this.apiMsgData.parameterized;
            },
            monitorSetupHooks() {
                return this.apiMsgData.setupHooks;
            },
            monitorTeardownHooks() {
                return this.apiMsgData.teardownHooks;
            },

        },
        watch: {
            monitorParam: {
                handler: function () {
                    if (this.apiMsgData.param.length === 0) {
                        this.addTableRow('param')
                    } else if (this.apiMsgData.param[this.apiMsgData.param.length - 1]['key'] || this.apiMsgData.param[this.apiMsgData.param.length - 1]['value']) {
                        this.addTableRow('param')
                    }
                    let strParam = '';

                    for (let i in this.apiMsgData.param) {
                        if (parseInt(i) + 2 === this.apiMsgData.param.length && this.apiMsgData.param[i].key) {
                            if (this.apiMsgData.param[i].value) {
                                strParam += this.apiMsgData.param[i].key + '=' + this.apiMsgData.param[i].value;
                            } else {
                                strParam += this.apiMsgData.param[i].key;
                            }
                        } else if (this.apiMsgData.param[i].key) {
                            strParam += this.apiMsgData.param[i].key + '=' + this.apiMsgData.param[i].value + '&';
                        }
                    }
                    if (strParam.substr(strParam.length - 1, 1) === '&') {
                        strParam = strParam.substring(0, strParam.length - 1)
                    }
                    if (strParam) {
                        this.apiMsgData.url = this.apiMsgData.url.split("?")[0] + '?' + strParam
                    } else {
                        this.apiMsgData.url = this.apiMsgData.url.split("?")[0]
                    }

                },
                deep: true
            },
            monitorUrl() {
                if (!this.apiMsgData.url) {
                    this.apiMsgData.param = [{key: '', value: ''}];
                    return
                }
                if (this.apiMsgData.url.indexOf('?') === -1) {
                    this.apiMsgData.param = [{key: '', value: ''}];
                    return
                }

                let url = this.apiMsgData.url.split("?");
                url.splice(0, 1);
                url = url.join("?");
                if (!url) {
                    this.apiMsgData.param = [{key: '', value: ''}];
                    return
                }
                let strParam = url.split("&");
                if (strParam[0]) {
                    this.apiMsgData.param = Array();
                    for (let i = 0; i < strParam.length; i++) {
                        if (strParam[i].indexOf('=') !== -1) {
                            let _array = strParam[i].split("=");

                            let d = _array[0];
                            _array.splice(0, 1);

                            this.apiMsgData.param.push({
                                key: d,
                                value: _array.join("=")
                            });
                            // console.log(unescape(_array.join("=")))
                        } else {
                            this.apiMsgData.param.push({key: strParam[i], value: ''});
                        }
                    }
                }

            },
            monitorMethod(newValue) {
                if (newValue === 'GET') {
                    this.bodyShow = 'first'
                }
            },
            monitorVariable: {
                handler: function () {
                    if (this.apiMsgData.variable.length === 0) {
                        this.addTableRow('variable')
                    }
                    if (this.apiMsgData.variable[this.apiMsgData.variable.length - 1]['key'] || this.apiMsgData.variable[this.apiMsgData.variable.length - 1]['value']) {
                        this.addTableRow('variable')
                    }
                }
                ,
                deep: true
            },
            monitorExtract: {
                handler: function () {
                    if (this.apiMsgData.extract.length === 0) {
                        this.addTableRow('extract')
                    }
                    if (this.apiMsgData.extract[this.apiMsgData.extract.length - 1]['key'] || this.apiMsgData.extract[this.apiMsgData.extract.length - 1]['value']) {
                        this.addTableRow('extract')
                    }
                }
                ,
                deep: true
            },
            monitorHeader: {
                handler: function () {
                    if (this.apiMsgData.header.length === 0) {
                        this.addTableRow('header')
                    }
                    if (this.apiMsgData.header[this.apiMsgData.header.length - 1]['key'] || this.apiMsgData.header[this.apiMsgData.header.length - 1]['value']) {
                        this.addTableRow('header')
                    }
                }
                ,
                deep: true
            },
            monitorValidate: {
                handler: function () {
                    if (this.apiMsgData.validate.length === 0) {
                        this.addTableRow('validate')
                    }
                    if (this.apiMsgData.validate[this.apiMsgData.validate.length - 1]['key'] || this.apiMsgData.validate[this.apiMsgData.validate.length - 1]['value']) {
                        this.addTableRow('validate')
                    }
                }
                ,
                deep: true
            },

            monitorGlobalVar: {
                handler: function () {
                    if (this.apiMsgData.globalVar.length === 0) {
                        this.addTableRow('globalVar')
                    }
                    if (this.apiMsgData.globalVar[this.apiMsgData.globalVar.length - 1]['key'] ||
                        this.apiMsgData.globalVar[this.apiMsgData.globalVar.length - 1]['value']) {
                        this.addTableRow('globalVar')
                    }
                },
                deep: true
            },
            monitorParameterized: {
                handler: function () {
                    if (this.apiMsgData.parameterized.length === 0) {
                        this.addTableRow('parameterized')
                    }
                    if (this.apiMsgData.parameterized[this.apiMsgData.parameterized.length - 1]['key'] ||
                        this.apiMsgData.parameterized[this.apiMsgData.parameterized.length - 1]['value']) {
                        this.addTableRow('parameterized')
                    }
                },
                deep: true
            },
            monitorSetupHooks: {
                handler: function () {
                    if (this.apiMsgData.setupHooks.length === 0) {
                        this.addTableRow('setupHooks')
                    }
                    if (this.apiMsgData.setupHooks[this.apiMsgData.setupHooks.length - 1]['key']) {
                        this.addTableRow('setupHooks')
                    }
                }
                ,
                deep: true
            },
            monitorTeardownHooks: {
                handler: function () {
                    if (this.apiMsgData.teardownHooks.length === 0) {
                        this.addTableRow('teardownHooks')
                    }
                    if (this.apiMsgData.teardownHooks[this.apiMsgData.teardownHooks.length - 1]['key']) {
                        this.addTableRow('teardownHooks')
                    }
                }
                ,
                deep: true
            },

        },
    }
</script>

<style scoped>    
    .traceback, .validators {
    background: #f7f7f7;
    border: 2px solid #dedede;
    padding: 10px;
    margin: 5px 0;
    border-radius: 5px;
    }

    .validatorPre {
    margin: 0 !important;
    white-space:pre-wrap; /* css3.0 */
    white-space:-moz-pre-wrap; /* Firefox */
    white-space:-pre-wrap; /* Opera 4-6 */
    white-space:-o-pre-wrap; /* Opera 7 */
    word-wrap:break-word; /* Internet Explorer 5.5+ */
    }
    
    .drag-box {
        display: flex;
        user-select: none;
    }

    .drag-box-item {
        flex: 1;
        max-width: 330px;
        min-width: 300px;
        width: 300px;
        background-color: #eff1f5;
        margin-right: 16px;
        border-radius: 6px;
        border: 1px #e1e4e8 solid;
    }

    .drag-box-col{
        width: 300px;

    }

    .form-box{
        width: 1500px;
    }

    .item-title {
        padding: 8px 8px 8px 12px;
        font-size: 14px;
        line-height: 1.5;
        color: #24292e;
        font-weight: 600;
    }

    .item-ul {
        padding: 0 8px 8px;
        height: 300px;
        overflow-y: scroll;
    }

    .item-ul::-webkit-scrollbar {
        width: 0;
    }

    .drag-list {
        border: 1px #e1e4e8 solid;
        padding: 10px;
        margin: 5px 0 10px;
        list-style: none;
        background-color: #fff;
        border-radius: 6px;
        cursor: pointer;
        -webkit-transition: border .3s ease-in;
        transition: border .3s ease-in;
    }

    .drag-list:hover {
        border: 1px solid #20a0ff;
    }

    .drag-title {
        font-weight: 400;
        line-height: 25px;
        margin: 10px 0;
        font-size: 22px;
        color: #1f2f3d;
    }

    .ghost-style {
        display: block;
        color: transparent;
        border-style: dashed
    }

    .el-row {
        margin-bottom: 20px;
        margin-top: 20px
    }

    .el-col {
        border-radius: 4px;
    }

    .h-b-e-a-style {
        background-color: rgb(250, 250, 250);
        /*min-height: 430px;*/
    }
</style>
