<template>
    <div class="table">
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-calendar"></i> 性能测试
                </el-breadcrumb-item>
                <el-breadcrumb-item>性能测试列表</el-breadcrumb-item>
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

                <router-link to="locusts_add">
                    <el-button type="primary" icon="el-icon-plus" class="handle-del mr10">新增性能测试</el-button>
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

                <el-table-column prop="name" label="性能测试名称" width="250"></el-table-column>
                <el-table-column prop="project" label="所属项目" sortable align="center"></el-table-column>

                <el-table-column prop="testcase_count" label="包含用例数" sortable align="center"></el-table-column>

                <el-table-column prop="create_time" label="创建时间" sortable align="center"></el-table-column>

                <el-table-column label="操作" align="center">
                    <template slot-scope="scope">
                        <el-button
                            type="text"
                            icon="el-icon-caret-right"
                            @click="handleRun(scope.$index, scope.row)"
                        >运行</el-button>
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
        <el-dialog title="删除性能测试" :visible.sync="delVisible" width="300px" center>
            <div class="del-dialog-cnt">删除不可恢复，是否确定删除？</div>
            <span slot="footer" class="dialog-footer">
                <el-button @click="delVisible = false">取 消</el-button>
                <el-button type="primary" @click="deleteRow">确 定</el-button>
            </span>
        </el-dialog>

        <el-dialog title="批量删除性能测试" :visible.sync="delAllVisible" width="300px" center>
            <div class="del-dialog-cnt">删除不可恢复，是否确定删除？</div>
            <span slot="footer" class="dialog-footer">
                <el-button @click="delAllVisible = false">取 消</el-button>
                <el-button type="primary" @click="delAll">确 定</el-button>
            </span>
        </el-dialog>

        <!-- 解除占用提示框 -->
        <el-dialog title="解除端口占用" :visible.sync="killVisible" width="300px" center>
            <div class="del-dialog-cnt">压测端口已被占用,是否解除占用？</div>
            <span slot="footer" class="dialog-footer">
                <el-button @click="killVisible = false">取 消</el-button>
                <el-button type="primary" @click="killPort">确 定</el-button>
            </span>
        </el-dialog>

        <!-- 运行项目弹出框 -->
        <el-dialog title="运行性能测试 " :visible.sync="runVisible" width="30%" center>
            <el-form ref="form" :model="form" label-width="120px">
                <el-form-item label="运行环境" prop="env_id" required>
                    <el-select v-model="form.env_id" clearable placeholder="请选择">
                        <el-option
                            v-for="item in envs_id_names"
                            :key="item.id"
                            :label="item.name"
                            :value="item.id"
                        ></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="无界面启动" prop="no_web">
                    <el-switch v-model="form.no_web"></el-switch>
                </el-form-item>

                <el-form-item v-show="form.no_web" label="模拟用户总数" prop="clients" required>
                    <el-input v-model.number="form.clients"></el-input>
                </el-form-item>

                <el-form-item v-show="form.no_web" label="每秒生成用户数" prop="hatch_rate" required>
                    <el-input v-model.number="form.hatch_rate"></el-input>
                </el-form-item>

                <el-form-item v-show="form.no_web" label="测试持续时间/s" prop="run_time" required>
                    <el-input v-model.number="form.run_time"></el-input>
                </el-form-item>

                <el-form-item label="逐步负载" prop="step_load">
                    <el-switch v-model="form.step_load"></el-switch>
                </el-form-item>

                <el-form-item
                    v-show="form.no_web && form.step_load"
                    label="每次加压用户数"
                    prop="step_clients"
                    required
                >
                    <el-input v-model.number="form.step_clients"></el-input>
                </el-form-item>

                <el-form-item
                    v-show="form.no_web && form.step_load"
                    label="加压成功后持续时间/s"
                    prop="step_time"
                    required
                >
                    <el-input v-model.number="form.step_time"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="runVisible = false">取 消</el-button>
                <el-button
                    type="primary"
                    @click="!form.no_web ? confirmRun() : confirmRunNoweb()"
                >运 行</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
import { locusts_list, locust_delete, envs_names, run_locust, kill_port, run_locust_noweb } from '../../api/api';
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
            runVisible: false,
            killVisible: false,
            form: {},

            idx: -1, // 在tableData数组中的索引值
            id: -1, // 在数据库中的真实索引值

            // env_id: '',
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
                    if (d.name.indexOf(this.select_word) > -1 || d.project.indexOf(this.select_word) > -1) {
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
            locusts_list({
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
                locust_delete(this.multipleSelection[i].id)
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
        killPort() {
            kill_port(this.id, this.env_id)
                .then((response) => {
                    this.$message.success('释放端口成功,正在启动新的性能测试!');
                    this.killVisible = false;
                    setTimeout(() => {
                        this.confirmRun();
                    }, 1000);
                })
                .catch((error) => {
                    this.$message.error('服务器错误');
                });
        },
        // 确定删除
        deleteRow() {
            locust_delete(this.id)
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
        confirmRun() {
            if (this.form.env_id) {
                run_locust(this.id, this.form)
                    .then((response) => {
                        if (response.data.code == 2) {
                            this.$router.push({ name: 'locust_view', query: { locust_url: response.data.url } });
                            this.runVisible = false;
                        } else if (response.data.code == 3) {
                            this.runVisible = false;
                            this.killVisible = true;
                        }
                    })
                    .catch((error) => {
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
        confirmRunNoweb() {
            if (this.form.env_id) {
                run_locust_noweb(this.id, this.form).catch((error) => {
                    if (typeof error === 'object' && error.hasOwnProperty('msg')) {
                        this.$message.error(error.msg + '-----运行中断');
                    } else {
                        this.$message.error('服务器错误' + '-----运行中断');
                    }
                });
                this.runVisible = false;
                this.$message.success('性能测试已运行,稍后会有邮件提醒');
            } else {
                this.$message.error('请选择运行环境');
            }
        },
        linkTo(id) {
            this.$router.push({ path: `/locusts_edit/${id}` });
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
