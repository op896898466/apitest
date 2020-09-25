<template>
    <div class="table">
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-calendar"></i> Mock管理
                </el-breadcrumb-item>
                <el-breadcrumb-item>Mock接口列表</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <div class="handle-box">
                <el-button type="primary" icon="el-icon-delete" @click="delAllVisible = true">批量删除</el-button>

                <el-button type="primary" icon="el-icon-plus" @click="addVisible = true">新增Mock接口</el-button>

                <el-input v-model="select_word" placeholder="输入筛选关键词" class="handle-input mr10"></el-input>
                <el-button
                    type="primary"
                    icon="el-icon-refresh-right"
                    style="float:right"
                    @click="restart()"
                >重启Mock</el-button>
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

                <el-table-column prop="name" label="接口名称" width="250"></el-table-column>

                <el-table-column prop="uri" label="uri" sortable align="center"></el-table-column>

                <el-table-column prop="description" label="简要描述" sortable align="center"></el-table-column>

                <el-table-column prop="mocks" label="场景数" sortable align="center"></el-table-column>

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

                <el-table-column prop="create_time" label="创建时间" sortable align="center"></el-table-column>

                <el-table-column label="操作" align="center">
                    <template slot-scope="scope">
                        <el-button
                            type="text"
                            icon="el-icon-s-promotion"
                            @click="linkTo(scope.row.id)"
                        >进入</el-button>
                        <el-button type="text" icon="el-icon-edit" @click="handleEdit(scope.row)">编辑</el-button>
                        <el-button
                            type="text"
                            icon="el-icon-delete"
                            class="red"
                            @click="handleDelete(scope.$index, scope.row)"
                        >删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <br>
            <p style="float:right"><font size="3" color="#ADADAD">备注：Mock服务的默认端口为8899</font></p>
            <br>
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
        <el-dialog title="删除Mock接口" :visible.sync="delVisible" width="300px" center>
            <div class="del-dialog-cnt">删除不可恢复，是否确定删除？</div>
            <span slot="footer" class="dialog-footer">
                <el-button @click="delVisible = false">取 消</el-button>
                <el-button type="primary" @click="deleteRow">确 定</el-button>
            </span>
        </el-dialog>

        <el-dialog title="批量删除Mock接口" :visible.sync="delAllVisible" width="300px" center>
            <div class="del-dialog-cnt">删除不可恢复，是否确定删除？</div>
            <span slot="footer" class="dialog-footer">
                <el-button @click="delAllVisible = false">取 消</el-button>
                <el-button type="primary" @click="delAll">确 定</el-button>
            </span>
        </el-dialog>

        <!-- 新增弹出框 -->
        <el-dialog title="新增Mock接口" :visible.sync="addVisible" width="30%" center>
            <el-form ref="form" :model="form" :rules="rules" label-width="120px">
                <!-- <el-form-item label="日期">
                    <el-date-picker type="date" placeholder="选择日期" v-model="form.date" value-format="yyyy-MM-dd" style="width: 100%;"></el-date-picker>
                </el-form-item>-->
                <el-form-item label="接口名称" prop="name" required>
                    <el-input v-model="form.name" clearable></el-input>
                </el-form-item>

                <el-form-item label="uri" prop="uri" required>
                    <el-input v-model="form.uri" placeholder="/example" clearable></el-input>
                </el-form-item>

                <el-form-item label="简要描述" prop="description">
                    <el-input v-model="form.description" clearable></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button @click="cancelAdd">取消</el-button>
                    <el-button type="primary" @click="confirmAdd('form')">提交</el-button>
                </el-form-item>
            </el-form>
        </el-dialog>

        <!-- 编辑弹出框 -->
        <el-dialog title="编辑Mock接口" :visible.sync="editVisible" width="30%" center>
            <el-form ref="editForm" :model="editForm" :rules="rules" label-width="120px">
                <!-- <el-form-item label="日期">
                    <el-date-picker type="date" placeholder="选择日期" v-model="form.date" value-format="yyyy-MM-dd" style="width: 100%;"></el-date-picker>
                </el-form-item>-->
                <el-form-item label="接口名称" prop="name" required>
                    <el-input v-model="editForm.name" clearable></el-input>
                </el-form-item>

                <el-form-item label="uri" prop="uri" required>
                    <el-input v-model="editForm.uri" placeholder="/example" clearable></el-input>
                </el-form-item>

                <el-form-item label="简要描述" prop="description">
                    <el-input v-model="editForm.description" clearable></el-input>
                </el-form-item>

                <el-form-item label="是否启用" prop="enabled">
                    <el-switch v-model="editForm.enabled"></el-switch>
                </el-form-item>

                <el-form-item>
                    <el-button @click="cancelEdit">取消</el-button>
                    <el-button type="primary" @click="confirmEdit('editForm')">提交</el-button>
                </el-form-item>
            </el-form>
        </el-dialog>
    </div>
</template>

<script>
import {
    interfacemock_list,
    get_detail_interfacemock,
    add_interfacemock,
    update_interfacemock,
    patch_interfacemock,
    delele_interfacemock,
    restart_mock
} from '../../api/api';
import { Loading } from 'element-ui';
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
            editVisible: false,
            delVisible: false,
            delAllVisible: false,
            addVisible: false,
            form: {
                name: '',
                uri: '',
                description: '',
                enabled: false
            },
            editForm: {
                name: '',
                uri: '',
                description: '',
                enabled: false
            },
            rules: {
                name: [{ required: true, message: '请输入Mock借口名称', trigger: 'blur' }],
                uri: [
                    { required: true, message: '请输入合法的uri', trigger: 'blur' },
                    { pattern: /^\/[A-Za-z0-9\/(\+~%\/\.\w\-_)*]+$/, message: '请输入合法的uri' }
                ]
            },

            idx: -1, // 在tableData数组中的索引值
            id: -1 // 在数据库中的真实索引值
        };
    },
    beforeRouteEnter(to, from, next) {
        // 在路由跳转页面实例化之前被调用, 此时还没有this实例, 但是可以通过next的回调中获取实例的引用
        next((vm) => {
            vm.getData(); // 获取数据
        });
        next();
    },
    // created() {
    //     this.getData(); // 获取项目数据
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
                    if (d.name.indexOf(this.select_word) > -1 || d.uri.indexOf(this.select_word) > -1) {
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
            interfacemock_list({
                page: this.cur_page,
                size: this.page_size
            }).then((response) => {
                this.tableData = response.data.results;
                this.cur_page = response.data.current_page_num || 1;
                this.total_nums = response.data.count || 1;
            });
        },
        handleRun(index, row) {
            this.idx = index; // 当前修改的数据, 在tableData数组中的索引值
            this.id = row.id; // 当前修改的数据在数据库中的真实索引值
            this.form = row;
            this.runVisible = true;
        },
        handleEdit(row) {
            this.editForm = row;
            this.editVisible = true;
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
                delele_interfacemock(this.multipleSelection[i].id)
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
        changeSwitch(row) {
            patch_interfacemock(row.id, { enabled: row.enabled })
                .then((response) => {
                    if (row.enabled) {
                        this.$message.success('Mock接口启用成功');
                    } else {
                        this.$message.warning('Mock接口禁用成功');
                    }
                })
                .catch((error) => {
                    this.$message.error('服务器错误');
                    this.getData();
                });
        },
        // 新增
        confirmAdd(form) {
            this.$refs[form].validate((valid) => {
                if (valid) {
                    add_interfacemock(this.form)
                        .then((response) => {
                            this.$message.success('新增成功');
                            this.addVisible = false;
                            this.getData();
                            this.$refs['form'].resetFields();
                        })
                        .catch((error) => {
                            if (typeof error === 'object' && error.hasOwnProperty('name')) {
                                this.$message.error(error.name[0]);
                            } else {
                                this.$message.error('服务器错误');
                            }
                        });
                }
            });
        },
        cancelAdd() {
            this.addVisible = false;
            this.$refs['form'].resetFields();
        },
        // 编辑
        confirmEdit(form) {
            this.$refs[form].validate((valid) => {
                if (valid) {
                    update_interfacemock(this.editForm.id, this.editForm)
                        .then((response) => {
                            this.$message.success('修改成功');
                            this.editVisible = false;
                            this.getData();
                            // this.$refs[form].resetFields();
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
        },
        restart() {
            let loadingInstance = Loading.service({ fullscreen: true, text: '请稍等', background: 'rgba(0, 0, 0, 0.8)' });
            restart_mock()
                .then((response) => {
                    loadingInstance.close();
                    if (response.data.code == 1) {
                        this.$message.success(response.data.msg);
                    } else {
                        this.$message.error(response.data.msg);
                    }
                })
                .catch((error) => {
                    loadingInstance.close();
                    this.$message.error('服务器错误');
                });
        },
        search() {
            this.is_search = true;
        },
        cancelEdit() {
            this.editVisible = false;
        },
        deleteRow() {
            delele_interfacemock(this.id)
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
        linkTo(id) {
            this.$router.push({ path: `/interfacemocks/${id}` });
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
