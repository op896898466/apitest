<template>
    <div class="table">
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-calendar"></i> Mock管理
                </el-breadcrumb-item>
                <el-breadcrumb-item>Mock详情</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <el-row>
            <el-col :span="24">
                <div class="grid-content bg-purple-dark">
                    <strong>接口详情：</strong>
                </div>
            </el-col>
        </el-row>
        <el-row :gutter="20">
            <el-col :span="6">
                <div class="grid-content bg-purple">接口名：{{interfacemock.name}}</div>
            </el-col>
            <el-col :span="6">
                <div class="grid-content bg-purple">uri：{{interfacemock.uri}}</div>
            </el-col>
            <el-col :span="6">
                <div class="grid-content bg-purple">描述：{{interfacemock.description}}</div>
            </el-col>
            <el-col :span="6">
                <div class="grid-content bg-purple">状态：{{interfacemock.enabled}}</div>
            </el-col>
        </el-row>
        <div class="container">
            <div class="handle-box">
                <!-- <el-button
                    type="primary"
                    icon="el-icon-delete"
                    class="handle-del mr10"
                    @click="delAllVisible = true"
                >批量删除</el-button>-->

                <el-button
                    type="primary"
                    icon="el-icon-plus"
                    class="handle-del mr10"
                    @click="addVisible = true"
                >新增Mock接口</el-button>
            </div>
            <el-table :data="mocks" border class="table" ref="multipleTable" stripe>
                <!-- <el-table-column type="selection" width="55" align="center"></el-table-column> -->

                <el-table-column type="index" label="序号" width="55" align="center"></el-table-column>

                <el-table-column prop="name" label="场景名" width="250"></el-table-column>

                <el-table-column prop="description" label="简要描述" sortable align="center"></el-table-column>

                <el-table-column label="状态">
                    <template slot-scope="scope">
                        <el-switch
                            v-model="scope.row.enabled"
                            active-color="#2d8cf0"
                            inactive-color="#B9B9B9"
                            @change="changeSwitch(scope.row)"
                        />
                    </template>
                </el-table-column>

                <el-table-column label="操作" align="center">
                    <template slot-scope="scope">
                        <el-button
                            type="text"
                            icon="el-icon-edit"
                            @click="handleEdit(scope.row.id)"
                        >编辑</el-button>
                        <el-button
                            type="text"
                            icon="el-icon-delete"
                            class="red"
                            @click="handleDelete(scope.$index, scope.row)"
                        >删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <!-- 删除提示框 -->
        <el-dialog title="删除Mock场景" :visible.sync="delVisible" width="300px" center>
            <div class="del-dialog-cnt">删除不可恢复，是否确定删除？</div>
            <span slot="footer" class="dialog-footer">
                <el-button @click="delVisible = false">取 消</el-button>
                <el-button type="primary" @click="deleteRow">确 定</el-button>
            </span>
        </el-dialog>

        <el-dialog
            title="新增Mock场景"
            :visible.sync="addVisible"
            width="800px"
            :close-on-click-modal="false"
            center
        >
            <el-form :model="addMockInfo" ref="addMockInfo" :rules="rules" label-width="100px">
                <el-row>
                    <el-col :span="8">
                        <el-form-item label="场景名" prop="name">
                            <el-input v-model="addMockInfo.name"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="15">
                        <el-form-item label="简要描述" prop="description">
                            <el-input v-model="addMockInfo.description"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-form-item label="请求数据" prop="request">
                        <editor
                                style="font-size: 15px"
                                v-model="addMockInfo.request"
                                @init="editorInit"
                                lang="json"
                                theme="monokai"
                                width="100%"
                                height="200px"
                                :options="{}"
                        >
                        </editor>
                    </el-form-item>
                </el-row>
                <el-row>
                    <el-form-item label="响应数据" prop="response">
                        <editor
                                style="font-size: 15px"
                                v-model="addMockInfo.response"
                                @init="editorInit"
                                lang="json"
                                theme="monokai"
                                width="100%"
                                height="200px"
                                :options="{}"
                        >
                        </editor>
                    </el-form-item>
                </el-row>
                <el-row>
                    <el-button type="primary" size="mini"
                            style="float:right;margin-left:20px"
                            @click="formatData('addMockInfo')">格式化

                    </el-button>
                </el-row>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="addVisible = false">取 消</el-button>
                <el-button type="primary" @click="addMock('addMockInfo')">确 定</el-button>
            </span>
        </el-dialog>

        <el-dialog
            title="编辑Mock场景"
            :visible.sync="editVisible"
            width="800px"
            :close-on-click-modal="false"
            center
        >
            <el-form :model="editMockInfo" ref="editMockInfo" :rules="rules" label-width="100px">
                <el-row>
                    <el-col :span=8 >
                        <el-form-item label="场景名" prop="name">
                            <el-input v-model="editMockInfo.name"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span=15 >
                        <el-form-item label="简要描述" prop="description">
                            <el-input v-model="editMockInfo.description"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-form-item label="请求数据" prop="request">
                        <editor
                                style="font-size: 15px"
                                v-model="editMockInfo.request"
                                @init="editorInit"
                                lang="json"
                                theme="monokai"
                                width="100%"
                                height="200px"
                                :options="{}"
                        >
                        </editor>
                    </el-form-item>
                </el-row>
                <el-row>
                    <el-form-item label="响应数据" prop="response">
                        <editor
                                style="font-size: 15px"
                                v-model="editMockInfo.response"
                                @init="editorInit"
                                lang="json"
                                theme="monokai"
                                width="100%"
                                height="200px"
                                :options="{}"
                        >
                        </editor>
                    </el-form-item>
                </el-row>
                <el-row>
                    <el-button type="primary" size="mini"
                            style="float:right;margin-left:20px"
                            @click="formatData('editMockInfo')">格式化

                    </el-button>
                </el-row>
                <el-row>
                    <el-form-item label="是否启用" prop="enabled">
                        <el-switch v-model="editMockInfo.enabled"></el-switch>
                    </el-form-item>
                </el-row>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editVisible = false">取 消</el-button>
                <el-button type="primary" @click="editMock('editMockInfo')">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
import draggable from 'vuedraggable';
import { mocks_list, get_detail_mock, add_mock, patch_mock, update_mock, delele_mock } from '../../api/api';
export default {
    components: {
        draggable,
        editor: require('vue2-ace-editor')   
    },
    beforeRouteEnter(to, from, next) {
        next((vm) => {
            vm.interfacemock_id = vm.$route.params.id;
            vm.getInterfacemockDetail();
        });
        next();
    },
    beforeRouteUpdate(to, from, next) {
        this.interfacemock_id = to.params.id;
        this.getInterfacemockDetail();
        next();
    },
    name: 'baseform',
    data: function () {
        return {
            interfacemock_id: null,
            mock_id: null,
            name: null,
            tester: null,
            desc: null,

            interfacemock: {},
            addMockInfo: {
                name: '',
                description: '',
                request: '{}',
                response: '{}',
                enabled: false
                // interface: this.interfaceInfo.id #发请求时再添加
            },
            editMockInfo: {
                name: '',
                description: '',
                request: '{}',
                response: '{}'
            },
            newRequest: '',
            requestChangeStatus: false,
            newResponse: '',
            responseChangeStatus: false,
            rules: {
                name: [
                    {
                        required: true,
                        message: '必填',
                        trigger: 'blur'
                    }
                ]
            },
            mocks: [],
            multipleSelection: [],
            // select_cate: '',
            select_word: '',
            del_list: [],
            addVisible: false,
            editVisible: false,
            delVisible: false
        };
    },

    created() {},
    methods: {
        handleDelete(index, row) {
            this.idx = index;
            this.id = row.id;
            this.delVisible = true;
        },
        changeSwitch(row) {
            patch_mock(row.id, { enabled: row.enabled })
                .then((response) => {
                    if (row.enabled) {
                        this.$message.success('Mock接口启用成功');
                    } else {
                        this.$message.warning('Mock接口禁用成功');
                    }
                })
                .catch((error) => {
                    this.$message.error('服务器错误');
                    this.getInterfacemockDetail();
                });
        },
        deleteRow() {
            delele_mock(this.id)
                .then((response) => {
                    // 项目删除成功
                    this.$message.success('删除成功');
                    this.delVisible = false;
                    this.mocks.splice(this.idx, 1);
                })
                .catch((error) => {
                    this.$message.error('服务器错误');
                });
        },
        // handleRequestJson(data) {
        //     this.requestChangeStatus = true;
        //     this.newRequest = data;
        // },
        // handleResponseJson(data) {
        //     this.responseChangeStatus = true;
        //     this.newResponse = data;
        // },
        // resetData() {
        //     this.requestChangeStatus = false;
        //     this.responseChangeStatus = false;
        //     this.newRequest = '';
        //     this.newResponse = '';
        // },
        checkReqAndResp(dataFlag, form) {
            // 数据被修改
            let dataNotEmpty = '数据不能为空';
            let dataError = '数据格式非正确json格式';
            let word = dataFlag === 'request' ? '请求' : '响应';
            let data = form === 'addMockInfo' ? this.addMockInfo[dataFlag].trim() : this.editMockInfo[dataFlag].trim();
            if (data === '') {
                this.$message.error(word + dataNotEmpty);
                return false;
            }
            if (!this.validateJson(data)) {
                this.$message.error(word + dataError);

                return false;
            } else if (dataFlag == "request") {
                let request_keys = [
                    'method',
                    'headers',
                    'json',
                    'factory',
                    'text',
                    'cookies',
                    'xpaths',
                    'json_paths',
                    'version',
                    'file',
                    'queries',
                    'path_resource',
                    'forms'
                ];
                let request_data = JSON.parse(data);
                for (let key in request_data) {
                    if (request_keys.indexOf(key) == -1) {
                        this.$message.error('请求数据不能包含:' + key);
                        return false;
                    }
                }
            } else {
                let response_keys = [
                    'attachment',
                    'headers',
                    'replay',
                    'json',
                    'text',
                    'proxy',
                    'cookies',
                    'record',
                    'status',
                    'version',
                    'file',
                    'latency',
                    'seq',
                    'cycle',
                    'path_resource'
                ];
                let  response_data = JSON.parse(data);
                for (let key in response_data) {
                    if (response_keys.indexOf(key) == -1) {
                        this.$message.error('响应数据不能包含:' + key);
                        return false;
                    }
                }
            }

            return true;
        },
        formatData(MockInfo) {
                // 格式化json字符串
                try {
                    
                    if(MockInfo=="addMockInfo"){
                        this.addMockInfo.request = JSON.parse(this.addMockInfo.request);
                        this.addMockInfo.request = JSON.stringify(this.addMockInfo.request, null, 4);
                        this.addMockInfo.response = JSON.parse(this.this.addMockInfo.response);
                        this.addMockInfo.response = JSON.stringify(this.addMockInfo.response, null, 4);

                    }else{
                        this.editMockInfo.request = JSON.parse(this.editMockInfo.request);
                        this.editMockInfo.request = JSON.stringify(this.editMockInfo.request, null, 4);
                        this.editMockInfo.response = JSON.parse(this.editMockInfo.response);
                        this.editMockInfo.response = JSON.stringify(this.editMockInfo.response, null, 4);

                    }

                } catch (err) {
                    this.$message({
                        showClose: true,
                        message: 'json格式错误',
                        type: 'warning',
                    });
                }
            },
        addMock(form) {
            this.$refs[form].validate((valid) => {
                if (valid) {
                    if (!this.checkReqAndResp('request', form) || !this.checkReqAndResp('response', form)) {
                        // 检查request和response是否为空,且格式是否正确
                        return;
                    }
                    this.addMockInfo.interfacemocks = this.interfacemock_id;
                    // 新增场景
                    add_mock(this.addMockInfo).then((data) => {
                        // 关闭弹窗 并刷新页面
                        this.addVisible = false;
                        this.getInterfacemockDetail();
                        this.$message.success('场景创建成功');
                        this.$refs[form].resetFields();
                        console.log(this.addMockInfo);
                        // this.addMockInfo = {
                        //     name: '',
                        //     description: '',
                        //     request: '{}',
                        //     response: '{}'
                        // };
                    });
                }
            });
        },
        editMock(form) {
            this.$refs[form].validate((valid) => {
                if (valid) {
                    if (!this.checkReqAndResp('request', form) || !this.checkReqAndResp('response', form)) {
                        // 检查request和response是否为空,且格式是否正确
                        return;
                    }
                    this.editMockInfo.interfacemocks = this.interfacemock_id;
                    // 新增场景
                    update_mock(this.editMockInfo.id, this.editMockInfo).then((data) => {
                        // 关闭弹窗 并刷新页面
                        this.editVisible = false;
                        this.getInterfacemockDetail();
                        this.$message.success('场景修改成功');
                        this.$refs[form].resetFields();
                        // this.addMockInfo = {
                        //     name: '',
                        //     description: '',
                        //     request: '{}',
                        //     response: '{}'
                        // };
                    });
                }
            });
        },
        validateJson(data) {
            // 判断是否为json格式的字串
            try {
                let a = JSON.parse(data);
                if(Object.prototype.toString.call(a) === '[object Object]'){
                    return true;

                }else{
                    return false;
                }
                
            } catch (e) {
                return false;
            }
        },

        handleEdit(id) {
            this.mock_id = id;
            get_detail_mock(this.mock_id)
                .then((response) => {
                    this.editMockInfo = response.data;
                })
                .catch((error) => {
                    this.$message.error('服务器错误');
                });
            this.editVisible = true;
        },
        clearValidate(prop_value) {
            this.$refs['form'].clearValidate(prop_value);
        },
        resetForm(formName) {
            this.$refs[formName].resetFields(); // 清空表单
        },
        getInterfacemockDetail() {
            mocks_list(this.interfacemock_id)
                .then((response) => {
                    this.interfacemock = response.data.interfacemock;
                    this.mocks = response.data.mocks_list;
                })
                .catch((error) => {
                    this.$message.error('服务器错误');
                });
        },
        editorInit() {
            require('brace/ext/language_tools');
            require('brace/mode/json');
            require('brace/theme/monokai');
            require('brace/snippets/json');
        }
    }
};
</script>

<style  scoped>
.el-row {
    margin-bottom: 10px;
}
.handle-box {
    margin-bottom: 20px;
}
.el-form-item label:after {
    content: '';
    display: inline-block;
    width: 100%;
}
</style>
