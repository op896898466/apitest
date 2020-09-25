<template>
    <div class="table">
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-calendar"></i> 用例管理
                </el-breadcrumb-item>
                <el-breadcrumb-item>用例列表</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <div class="handle-box">
                <el-button
                    type="primary"
                    icon="el-icon-delete"
                    class="handle-del mr10"
                    @click="delAllVisible = true"
                >批量删除</el-button>
                <router-link to="testcases_add">
                    <el-button type="primary" icon="el-icon-plus" class="handle-del mr10">新增用例</el-button>
                </router-link>
                <el-input v-model="select_word" placeholder="输入筛选关键词" class="handle-input mr10"></el-input>
            </div>
            <el-table
                :data="data"
                border
                class="table"
                ref="multipleTable"
                @selection-change="handleSelectionChange"
                stripe
            >
                <el-table-column type="selection" width="55" align="center"></el-table-column>

                <el-table-column type="index" label="序号" width="55" align="center"></el-table-column>

                <el-table-column prop="name" label="用例名称" width="250"></el-table-column>

                <el-table-column prop="module.project" label="所属项目" width="250"></el-table-column>

                <el-table-column prop="module.name" label="所属模块" width="250"></el-table-column>

                <el-table-column prop="author" label="测试人员" width="100" align="center"></el-table-column>

                <el-table-column label="操作" align="center">
                    <template slot-scope="scope">
                        <el-button
                            type="text"
                            icon="el-icon-caret-right"
                            @click="handleRun(scope.$index, scope.row)"
                        >运行</el-button>
                        <el-button
                            type="text"
                            icon="el-icon-copy-document"
                            @click="handleCopy(scope.row.id)"
                        >复制</el-button>
                        <el-button type="text" icon="el-icon-edit" @click="linkTo(scope.row.id)">编辑</el-button>
                        <el-button
                            type="text"
                            icon="el-icon-delete"
                            class="red"
                            @click="handleDelete(scope.$index, scope.row)"
                        >删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <div class="pagination">
                <el-pagination
                    background
                    @current-change="handleCurrentChange"
                    @size-change="handleSizeChange"
                    :page-sizes="[4, 5, 8, 10, 20]"
                    layout="total, sizes, prev, pager, next, jumper"
                    :total="total_nums"
                    :page-size="page_size"
                ></el-pagination>
            </div>
        </div>

        <!-- 删除提示框 -->
        <el-dialog title="删除用例" :visible.sync="delVisible" width="300px" center>
            <div class="del-dialog-cnt">删除不可恢复，是否确定删除？</div>
            <span slot="footer" class="dialog-footer">
                <el-button @click="delVisible = false">取 消</el-button>
                <el-button type="primary" @click="deleteRow">确 定</el-button>
            </span>
        </el-dialog>

        <el-dialog title="批量删除用例" :visible.sync="delAllVisible" width="300px" center>
            <div class="del-dialog-cnt">删除不可恢复，是否确定删除？</div>
            <span slot="footer" class="dialog-footer">
                <el-button @click="delAllVisible = false">取 消</el-button>
                <el-button type="primary" @click="delAll">确 定</el-button>
            </span>
        </el-dialog>

        <el-dialog title="复制用例" :visible.sync="copyVisible" width="300px" center>
            <el-form :model="copyForm" ref="copyForm" label-width="100px">
                <el-form-item
                    label="用例名称"
                    prop="name"
                    :rules="{ required: true, message: '用例名称不能为空'}"
                >
                    <el-input v-model="copyForm.name"></el-input>
                </el-form-item>

                <el-form-item>
                    <!-- <span slot="footer" class="dialog-footer"> -->
                    <el-button @click="copyVisible = false">取 消</el-button>
                    <el-button type="primary" @click="saveCopy('copyForm')">确 定</el-button>
                    <!-- </span> -->
                </el-form-item>
            </el-form>
        </el-dialog>

        <!-- 运行项目弹出框 -->
        <el-dialog title="运行用例" :visible.sync="runVisible" width="30%" center>
            <el-form ref="form" :model="form" label-width="120px">
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
                <el-button @click="runVisible = false">取 消</el-button>
                <el-button type="success" @click="confirmRun">同步运行</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
import { testcases_list, delete_testcase, envs_names, run_by_testcase, copy_testcase } from '../../api/api';
import { Loading } from 'element-ui';
// import { O_RDONLY } from 'constants';
export default {
    name: 'basetable',
    data() {
        return {
            tableData: [],
            cur_page: 1, // 当前页
            page_size: 10, // 每页显示的数量
            total_nums: 1, // 数据总条数

            multipleSelection: [],
            // select_cate: '',
            select_word: '',
            del_list: [],
            // is_search: false,
            editVisible: false, // 新增项目弹框是否显示标识
            delVisible: false, // 删除项目弹框是否显示标识
            delAllVisible: false,
            runVisible: false, // 运行项目弹框是否显示标识
            copyVisible: false,
            copyForm: {
                name: ''
            },
            form: {},

            idx: -1, // 在tableData数组中的索引值
            id: -1, // 在数据库中的真实索引值

            env_id: '',
            envs_id_names: [] // 返回的环境变量数据
        };
    },
    beforeRouteEnter(to, from, next) {
        // 在路由跳转页面实例化之前被调用, 此时还没有this实例, 但是可以通过next的回调中获取实例的引用
        next((vm) => {
            vm.getData(); // 获取数据
            vm.getEnvsIdNames();
        });
        next();
    },
    // created() {
    //     this.getData(); // 获取项目数据
    //     this.getEnvsIdNames(); // 获取环境变量ID和名称
    // },
    computed: {
        data() {
            return this.tableData.filter((d) => {
                let is_del = false;
                for (let i = 0; i < this.del_list.length; i++) {
                    if (d.name === this.del_list[i].name) {
                        is_del = true;
                        break;
                    }
                }
                if (!is_del) {
                    if (
                        d.name.indexOf(this.select_word) > -1 ||
                        d.module.project.indexOf(this.select_word) > -1 ||
                        d.module.name.indexOf(this.select_word) > -1 ||
                        d.author.indexOf(this.select_word) > -1
                    ) {
                        return d;
                    }
                }
            });
        }
    },
    methods: {
        // 分页导航
        handleCurrentChange(val) {
            this.cur_page = val;
            this.getData();
        },
        handleSizeChange(val) {
            this.page_size = val;
            this.getData();
        },
        getData() {
            testcases_list({
                page: this.cur_page,
                size: this.page_size
            }).then((response) => {
                this.tableData = response.data.results;
                this.cur_page = response.data.current_page_num || 1;
                this.total_nums = response.data.count || 1;
            });
        },
        search() {
            this.is_search = true;
        },
        formatter(row, column) {
            return row.address;
        },
        filterTag(value, row) {
            return row.tag === value;
        },
        handleEdit(index, row) {
            this.idx = index; // 当前修改的数据, 在tableData数组中的索引值
            this.id = row.id; // 当前修改的数据在数据库中的真实索引值
            this.form = row;
            this.editVisible = true;
        },
        handleRun(index, row) {
            this.idx = index; // 当前修改的数据, 在tableData数组中的索引值
            this.id = row.id; // 当前修改的数据在数据库中的真实索引值
            this.form = row;
            this.runVisible = true;
        },
        handleDelete(index, row) {
            this.idx = index;
            this.id = row.id;
            this.delVisible = true;
        },
        delAll() {
            const length = this.multipleSelection.length;
            let str = '';
            this.del_list = this.del_list.concat(this.multipleSelection);
            for (let i = 0; i < length; i++) {
                str += this.multipleSelection[i].name + ' ';
                delete_testcase(this.multipleSelection[i].id)
                    .then((response) => {})
                    .catch((error) => {
                        this.$message.error('服务器错误');
                    });
            }

            if (length === 0) {
                this.$message.error('未选择要删除的条目!');
            } else {
                this.$message.success('删除了' + str);
                this.multipleSelection = [];
            }
            this.delAllVisible = false;
        },
        handleSelectionChange(val) {
            this.multipleSelection = val;
        },
        // 确定删除
        deleteRow() {
            delete_testcase(this.id)
                .then((response) => {
                    // 项目删除成功
                    this.$message.success('删除成功');
                    this.delVisible = false;
                    if (this.tableData[this.idx].id === this.id) {
                        this.tableData.splice(this.idx, 1);
                    } else {
                        for (let i = 0; i < this.tableData.length; i++) {
                            if (this.tableData[i].id === this.id) {
                                this.tableData.splice(i, 1);
                                return;
                            }
                        }
                    }
                })
                .catch((error) => {
                    this.$message.error('服务器错误');
                });
        },
        // 获取所有环境变量的ID和名称
        getEnvsIdNames() {
            envs_names()
                .then((response) => {
                    this.envs_id_names = response.data; // 将返回的环境变量数据赋值给envs_id_names
                })
                .catch((error) => {
                    this.$message.error('服务器错误');
                });
        },
        //
        confirmRun() {
            if (this.env_id) {
                let datas = this.env_id;
                this.runVisible = false;
                let loadingInstance = Loading.service({ fullscreen: true, text: '加载中', background: 'rgba(0, 0, 0, 0.8)' });
                run_by_testcase(this.id, datas)
                    .then((response) => {
                        loadingInstance.close();
                        this.$router.push({ path: `/reports_view/${response.data.id}` });
                    })
                    .catch((error) => {
                        loadingInstance.close();
                        // console.log(error);
                        if (typeof error === 'object' && error.hasOwnProperty('msg')) {
                            this.$message.error(error.msg);
                        } else {
                            this.$message.error('服务器错误');
                        }
                    });
            } else {
                this.$message.error('请选择运行环境');
            }
        },
        linkTo(id) {
            this.$router.push({ path: `/testcases_edit/${id}` });
        },
        handleCopy(id) {
            this.id = id;
            this.copyVisible = true;
        },
        saveCopy(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    copy_testcase(this.id, this.copyForm.name)
                        .then((response) => {
                            this.$message.success('用例复制成功');
                            this.copyVisible = false;
                            this.$router.push({ path: `/testcases_edit/${response.data.id}` });
                        })
                        .catch((error) => {
                            if (typeof error === 'object' && error.hasOwnProperty('msg')) {
                                this.$message.error(error.msg);
                            } else {
                                this.$message.error('服务器错误');
                            }
                        });
                }
            });
        }
    }
};
</script>

<style scoped>
.handle-box {
    margin-bottom: 20px;
}

.handle-select {
    width: 120px;
}

.handle-input {
    width: 300px;
    display: inline-block;
}
.del-dialog-cnt {
    font-size: 16px;
    text-align: center;
}
.table {
    width: 100%;
    font-size: 14px;
}
.red {
    color: #ff0000;
}
.mr10 {
    margin-right: 10px;
}
</style>
