<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-calendar"></i> 配置管理
                </el-breadcrumb-item>
                <el-breadcrumb-item>新增配置</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-tabs type="border-card">
                <!--<el-tab-pane label="请求信息">-->

                <!--<el-tabs style="margin: 0 0 0 10px" v-model="bodyShow">-->
                <!--<el-tab-pane label="Headers" name="first">-->
                <!--<el-table :data="apiMsgData.header" size="mini" stripe :show-header="false"-->
                <!--class="h-b-e-a-style"-->
                <!--:row-style="{'background-color': 'rgb(250, 250, 250)'}">-->
                <!--<el-table-column property="key" label="Key" header-align="center" minWidth="100">-->
                <!--<template slot-scope="scope">-->
                <!--<el-input v-model="scope.row.key" size="mini" placeholder="key">-->
                <!--</el-input>-->
                <!--</template>-->
                <!--</el-table-column>-->

                <!--<el-table-column property="value" label="Value" header-align="center" minWidth="200">-->
                <!--<template slot-scope="scope">-->
                <!--<el-input v-model="scope.row.value" size="mini" placeholder="value">-->
                <!--</el-input>-->
                <!--</template>-->
                <!--</el-table-column>-->
                <!--<el-table-column property="value" label="操作" header-align="center" width="80">-->
                <!--<template slot-scope="scope">-->
                <!--<el-button type="danger" icon="el-icon-delete" size="mini"-->
                <!--@click.native="delTableRow('header',scope.$index)">-->
                <!--</el-button>-->
                <!--</template>-->
                <!--</el-table-column>-->
                <!--</el-table>-->
                <!--</el-tab-pane>-->
                <!--</el-tabs>-->

                <!--<el-tabs style="margin: 0 0 0 10px" v-model="otherShow">-->
                <!--<el-tab-pane label="环境变量" name="first">-->
                <!--<el-table :data="apiMsgData.globalVar" size="mini" stripe :show-header="false"-->
                <!--class="h-b-e-a-style"-->
                <!--:row-style="{'background-color': 'rgb(250, 250, 250)'}">-->
                <!--<el-table-column property="key" label="Key" header-align="center" minWidth="100">-->
                <!--<template slot-scope="scope">-->
                <!--<el-input v-model="scope.row.key" size="mini" placeholder="key">-->
                <!--</el-input>-->
                <!--</template>-->
                <!--</el-table-column>-->

                <!--<el-table-column label="type" header-align="center" width="100">-->
                <!--<template slot-scope="scope">-->
                <!--<el-select v-model="scope.row.param_type" size="mini">-->
                <!--<el-option v-for="item in paramTypes" :key="item" :value="item">-->
                <!--</el-option>-->
                <!--</el-select>-->
                <!--</template>-->
                <!--</el-table-column>-->

                <!--<el-table-column property="value" label="Value" header-align="center" minWidth="200">-->
                <!--<template slot-scope="scope">-->
                <!--<el-input v-model="scope.row.value" size="mini" placeholder="value">-->
                <!--</el-input>-->
                <!--</template>-->
                <!--</el-table-column>-->
                <!--<el-table-column property="value" label="操作" header-align="center" width="80">-->
                <!--<template slot-scope="scope">-->
                <!--<el-button type="danger" icon="el-icon-delete" size="mini"-->
                <!--@click.native="delTableRow('globalVar',scope.$index)">-->
                <!--</el-button>-->
                <!--</template>-->
                <!--</el-table-column>-->
                <!--</el-table>-->
                <!--</el-tab-pane>-->
                <!--</el-tabs>-->

                <!--&lt;!&ndash;</div>&ndash;&gt;-->
                <!--</el-tab-pane>-->

                <el-tab-pane label="请求头|全局变量">
                    <el-tabs style="margin: 0 0 0 10px" v-model="otherShow">
                        <el-tab-pane label="Headers" name="first">
                            <el-table
                                :data="apiMsgData.header"
                                size="mini"
                                stripe
                                :show-header="false"
                                class="h-b-e-a-style"
                                :row-style="{'background-color': 'rgb(250, 250, 250)'}"
                            >
                                <el-table-column
                                    property="key"
                                    label="Key"
                                    header-align="center"
                                    minWidth="100"
                                >
                                    <template slot-scope="scope">
                                        <el-input
                                            v-model="scope.row.key"
                                            size="mini"
                                            placeholder="key"
                                        ></el-input>
                                    </template>
                                </el-table-column>

                                <el-table-column
                                    property="value"
                                    label="Value"
                                    header-align="center"
                                    minWidth="200"
                                >
                                    <template slot-scope="scope">
                                        <el-input
                                            v-model="scope.row.value"
                                            size="mini"
                                            placeholder="value"
                                        ></el-input>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                    property="value"
                                    label="操作"
                                    header-align="center"
                                    width="80"
                                >
                                    <template slot-scope="scope">
                                        <el-button
                                            type="danger"
                                            icon="el-icon-delete"
                                            size="mini"
                                            @click.native="delTableRow('header',scope.$index)"
                                        ></el-button>
                                    </template>
                                </el-table-column>
                            </el-table>
                        </el-tab-pane>
                        <el-tab-pane label="全局变量" name="second">
                            <el-table
                                :data="apiMsgData.globalVar"
                                size="mini"
                                stripe
                                :show-header="false"
                                class="h-b-e-a-style"
                                :row-style="{'background-color': 'rgb(250, 250, 250)'}"
                            >
                                <el-table-column
                                    property="key"
                                    label="Key"
                                    header-align="center"
                                    minWidth="100"
                                >
                                    <template slot-scope="scope">
                                        <el-input
                                            v-model="scope.row.key"
                                            size="mini"
                                            placeholder="key"
                                        ></el-input>
                                    </template>
                                </el-table-column>

                                <el-table-column label="type" header-align="center" width="100">
                                    <template slot-scope="scope">
                                        <el-select v-model="scope.row.param_type" size="mini">
                                            <el-option
                                                v-for="item in paramTypes"
                                                :key="item"
                                                :value="item"
                                            ></el-option>
                                        </el-select>
                                    </template>
                                </el-table-column>

                                <el-table-column
                                    property="value"
                                    label="Value"
                                    header-align="center"
                                    minWidth="200"
                                >
                                    <template slot-scope="scope">
                                        <el-input
                                            v-model="scope.row.value"
                                            size="mini"
                                            placeholder="value"
                                        ></el-input>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                    property="value"
                                    label="操作"
                                    header-align="center"
                                    width="80"
                                >
                                    <template slot-scope="scope">
                                        <el-button
                                            type="danger"
                                            icon="el-icon-delete"
                                            size="mini"
                                            @click.native="delTableRow('globalVar',scope.$index)"
                                        ></el-button>
                                    </template>
                                </el-table-column>
                            </el-table>
                        </el-tab-pane>
                    </el-tabs>
                </el-tab-pane>
            </el-tabs>

            <el-row>
                <el-col :span="2">
                    <el-button type="primary" @click="onSubmit()">提交</el-button>
                </el-col>
                <el-col :span="2">
                    <el-button @click="close_page()">取消</el-button>
                </el-col>
            </el-row>
        </div>

        <!-- 编辑弹出框 -->
        <el-dialog title="创建配置" :visible.sync="editVisible" width="28%" center>
            <el-form label-width="120px">
                <el-form-item label="配置名称" required>
                    <el-input v-model="configure_name" clearable></el-input>
                </el-form-item>

                <el-form-item label="编写人员" required>
                    <el-input v-model="author" clearable></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveEdit">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
import { add_configure } from '../../api/api';
import bus from '../common/bus';
export default {
    name: 'baseform',
    data: function () {
        return {
            editVisible: false, // 新增配置弹框是否显示标识
            apiMsgData: {
                id: null,
                name: '',
                header: [{ key: null, value: null }],
                globalVar: [{ key: null, value: null, param_type: 'string' }]
            },
            bodyShow: 'second',
            otherShow: 'first',
            paramTypes: ['string', 'int', 'float', 'boolean'],
            cell: Object(),
            selected_configure_id: null,
            configure_name: null, // 配置名称
            author: '', // 用例编写人员
            configures: []
        };
    },
    methods: {
        close_page() {
            // this.apiMsgData= this.apiMsgDataInit;
            this.$router.go(-1);
            bus.$emit('close_current_tags');
        },
        onSubmit() {
            this.editVisible = true;
        },
        // 处理数据1, 有param_type, 返回js数组
        handleData1(request_data, msg) {
            let data_arr = [];
            for (let i = 0; i < request_data.length; i++) {
                let key = request_data[i].key;
                if (!key) {
                    this.$message.error(msg + '的key为空!');
                    return [];
                }
                let param_type = request_data[i].param_type;
                let value = request_data[i].value;
                if (param_type === 'int') {
                    if (/^\d+$/.test(value)) {
                        value = Number(value);
                    } else {
                        this.$message.error(msg + '不是整数int类型!');
                        return [];
                    }
                } else if (param_type === 'float') {
                    if (/^[+-]?\d+(\.\d+)?$/.test(value)) {
                        value = Number(value);
                    } else {
                        this.$message.error(msg + '不是小数float类型!');
                        return [];
                    }
                } else if (param_type === 'boolean') {
                    if (/^(true|True|TRUE|1|0)$/.test(value)) {
                        value = true;
                    } else if (/^(false|False|FALSE|0)$/.test(value)) {
                        value = false;
                    } else {
                        this.$message.error(msg + '不是布尔boolean类型!');
                        return [];
                    }
                }
                let one_data = {};
                one_data[key] = value;
                data_arr.push(one_data);
            }

            return data_arr;
        },

        // 处理数据2, 无param_type, 返回js对象
        handleData2(request_data, msg) {
            let one_data = {};
            for (let i = 0; i < request_data.length; i++) {
                let key = request_data[i].key;
                if (!key) {
                    this.$message.error(msg + '的key为空!');
                    return [];
                }
                one_data[key] = request_data[i].value;
            }
            return one_data;
        },

        // 保存编辑
        saveEdit() {
            if (this.configure_name === null) {
                this.$message.error('配置名称不能为空!');
                return;
            }

            if (this.author === '') {
                this.$message.error('编写人员名称不能为空!');
                return;
            }

            let datas = {
                name: this.configure_name, // 配置名称
                author: this.author, // 配置编写人员
                request: {
                    // 请求信息
                    config: {
                        request: {}
                    }
                }
            };

            // variables处理
            let variables = this.apiMsgData.globalVar;
            variables.splice(-1, 1);
            if (variables.length !== 0) {
                let new_data = this.handleData1(variables, '全局变量variables');
                if (new_data.length === 0) {
                    return;
                }
                datas.request.config['variables'] = new_data;
            }

            // headers处理
            let headers = this.apiMsgData.header;
            console.log(this.apiMsgData.header);
            headers.splice(-1, 1);
            if (headers.length !== 0) {
                let new_data = this.handleData2(headers, '请求头header');
                if (new_data.length === 0) {
                    return;
                }
                datas.request.config.request['headers'] = new_data;
            }

            // datas.include = JSON.stringify(datas.include);
            datas.request = JSON.stringify(datas.request);
            console.log(headers);
            add_configure(datas)
                .then((response) => {
                    this.editVisible = false;
                    let that = this;
                    this.$message.success(`新增配置成功`);
                    // 1秒钟之后, 执行刷新
                    this.close_page();
             
                })
                .catch((error) => {
                    this.editVisible = false;
                    if (typeof error === 'object' && error.hasOwnProperty('name')) {
                        console.log(error);
                        this.$message.error('配置名称已存在');
                    } else {
                        console.log(error);
                        this.$message.error('服务器错误');
                    }
                });
        },

        delTableRow(type, i) {
            if (type === 'variable') {
                this.apiMsgData.variable.splice(i, 1);
            } else if (type === 'header') {
                this.apiMsgData.header.splice(i, 1);
            } else if (type === 'param') {
                this.apiMsgData.param.splice(i, 1);
            } else if (type === 'globalVar') {
                this.apiMsgData.globalVar.splice(i, 1);
            } else if (type === 'parameterized') {
                this.apiMsgData.parameterized.splice(i, 1);
            } else if (type === 'setupHooks') {
                this.apiMsgData.setupHooks.splice(i, 1);
            } else if (type === 'teardownHooks') {
                this.apiMsgData.teardownHooks.splice(i, 1);
            }
        },
        addTableRow(type) {
            if (type === 'variable') {
                this.apiMsgData.variable.push({ key: null, value: null, param_type: 'string' });
            } else if (type === 'header') {
                this.apiMsgData.header.push({ key: null, value: null });
            } else if (type === 'param') {
                this.apiMsgData.param.push({ key: null, value: null });
            } else if (type === 'globalVar') {
                this.apiMsgData.globalVar.push({ key: null, value: null, param_type: 'string' });
            } else if (type === 'parameterized') {
                this.apiMsgData.parameterized.push({ key: null, value: null });
            } else if (type === 'setupHooks') {
                this.apiMsgData.setupHooks.push({ key: null });
            } else if (type === 'teardownHooks') {
                this.apiMsgData.teardownHooks.push({ key: null });
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
                    this.cell.style.height = i - 18 + 'px';
                } else {
                    this.cell.style.height = this.cell.scrollHeight + 'px';
                }
            }
        },
        querySearch(queryString, cb) {
            // 调用 callback 返回建议列表的数据
            cb(this.comparators);
        }
    },
    computed: {
        monitorHeader() {
            return this.apiMsgData.header;
        },

        monitorGlobalVar() {
            return this.apiMsgData.globalVar;
        }
    },
    watch: {
        monitorHeader: {
            handler: function () {
                if (this.apiMsgData.header.length === 0) {
                    this.addTableRow('header');
                }
                if (
                    this.apiMsgData.header[this.apiMsgData.header.length - 1]['key'] ||
                    this.apiMsgData.header[this.apiMsgData.header.length - 1]['value']
                ) {
                    this.addTableRow('header');
                }
            },
            deep: true
        },
        monitorGlobalVar: {
            handler: function () {
                if (this.apiMsgData.globalVar.length === 0) {
                    this.addTableRow('globalVar');
                }
                if (
                    this.apiMsgData.globalVar[this.apiMsgData.globalVar.length - 1]['key'] ||
                    this.apiMsgData.globalVar[this.apiMsgData.globalVar.length - 1]['value']
                ) {
                    this.addTableRow('globalVar');
                }
            },
            deep: true
        }
    }
};
</script>

<style scoped>
.drag-box {
    display: flex;
    user-select: none;
}

.drag-box-item {
    flex: 1;
    /* height: 300px; */
    max-width: 330px;
    min-width: 300px;
    background-color: #eff1f5;
    margin-right: 16px;
    border-radius: 6px;
    border: 1px #e1e4e8 solid;
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
    -webkit-transition: border 0.3s ease-in;
    transition: border 0.3s ease-in;
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
    border-style: dashed;
}

.el-row {
    margin-bottom: 20px;
    margin-top: 20px;
}

.el-col {
    border-radius: 4px;
}

.h-b-e-a-style {
    background-color: rgb(250, 250, 250);
    /*min-height: 430px;*/
}
</style>
