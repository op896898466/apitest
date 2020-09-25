<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-calendar"></i> 压力测试
                </el-breadcrumb-item>
                <el-breadcrumb-item>编辑压力测试</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <div class="form-box">
                <el-form label-position="left" label-width="120px">
                    <el-row :gutter="20">
                        <el-col :span="24">
                            <el-form-item label="选择项目">
                                <el-select
                                    v-model="selected_project_id"
                                    placeholder="请选择"
                                    @change="switchProject"
                                >
                                    <el-option
                                        v-for="(item, key) in project_names"
                                        :key="key"
                                        :label="item.name"
                                        :value="item.id"
                                    ></el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                    </el-row>

                    <el-row :gutter="20">
                        <el-col :span="24">
                            <el-form-item label=" 选择模块">
                                <el-select
                                    v-model="selected_module_id"
                                    placeholder="请选择"
                                    @change="getTestcaseByModuleID(selected_module_id)"
                                >
                                    <el-option
                                        v-for="(item, key) in modules"
                                        :key="key"
                                        :label="item.name"
                                        :value="item.id"
                                    ></el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                    </el-row>

                    <el-row :gutter="100">
                        <el-col :span="12">
                            <div class="drag-box-item">
                                <div class="item-title">待选用例</div>
                                <draggable v-model="unselected" :options="dragOptions">
                                    <transition-group tag="div" class="item-ul">
                                        <div
                                            v-for="item in unselected"
                                            class="drag-list"
                                            :key="item.id"
                                        >{{ item.name }}</div>
                                    </transition-group>
                                </draggable>
                            </div>
                        </el-col>

                        <el-col :span="12">
                            <div class="drag-box-item">
                                <div class="item-title">已选用例</div>
                                <draggable
                                    v-model="selected_testcase"
                                    :options="dragOptions"
                                    @change="changeResult()"
                                >
                                    <transition-group tag="div" class="item-ul">
                                        <div
                                            v-for="item in selected_testcase"
                                            class="drag-list"
                                            :key="item.id"
                                        >{{ item.name }}</div>
                                    </transition-group>
                                </draggable>
                            </div>
                        </el-col>
                    </el-row>

                    <el-form-item>
                        <el-button type="primary" @click="editVisible = true">提交</el-button>
                        <el-button @click="close_page()">取消</el-button>
                    </el-form-item>
                </el-form>
            </div>
        </div>
        <el-dialog title="编辑压力测试" :visible.sync="editVisible" width="28%" center>
            <el-form label-width="120px">
                <el-form-item label="压测名称" required>
                    <el-input v-model="name" clearable></el-input>
                </el-form-item>

                <el-form-item label="测试人员" required>
                    <el-input v-model="tester" clearable></el-input>
                </el-form-item>

                <el-form-item label="描述">
                    <el-input v-model="desc" clearable></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveEdit">确 定</el-button>
            </span>
        </el-dialog>
        <el-dialog title="是否切换项目" :visible.sync="switchVisible" width="300px" center>
            <div class="del-dialog-cnt">切换项目将清空已选用例，是否确定切换？</div>
            <span slot="footer" class="dialog-footer">
                <el-button @click="changeProjectCancle">取 消</el-button>
                <el-button type="primary" @click="getModulesByProjectID(selected_project_id)">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
import draggable from 'vuedraggable';
import { projects_names, modules_by_project_id, testcases_by_module_id, get_detail_locust, update_locust } from '../../api/api';
import bus from '../common/bus';
export default {
    beforeRouteEnter(to, from, next) {
        next((vm) => {
            vm.current_locust_id = vm.$route.params.id;
            vm.getLocustDetail();
        });
        next();
    },
    beforeRouteUpdate(to, from, next) {
        this.current_locust_id = to.params.id;
        this.vm.getLocustDetail();
        next();
    },
    name: 'baseform',
    data: function () {
        return {
            current_locust_id: null,
            name: null,
            tester: null,
            desc: null,
            project_names: [],
            modules: [],
            dragOptions: {
                animation: 120,
                scroll: true,
                group: 'sortlist',
                ghostClass: 'ghost-style'
            },
            selected_project_id: null,
            selected_module_id: null,
            switchVisible: false,
            editVisible: false,
            selected_testcase: [],
            unselected: []
        };
    },
    // watch: {
    //    selected: function() {
    //         var len = this.selected.length;
    //         var text = "[";
    //         for (var i = 0; i < len; i++) {
    //             console.log(this.selected[i].id);
    //             if (i == len-1) {
    //                 text += this.selected[i].id + "]";
    //             } else {
    //                 text += this.selected[i].id + ", ";
    //             }

    //         }
    //         if (len == 0){
    //             text = "[]";
    //         }
    //        this.form.include = text;
    //        console.log(this.form.include)
    //    }
    // },
    components: {
        draggable
    },
    created() {
        this.getProjectNames();
    },
    methods: {
        close_page() {
            this.$router.go(-1);
            bus.$emit('close_current_tags');
        },
        changeProjectCancle() {
            this.selected_project_id = this.beofore_selected_project;
            this.switchVisible = false;
        },
        getModulesByProjectID(pro_id) {
            this.beofore_selected_project = this.selected_project_id;
            modules_by_project_id(pro_id)
                .then((response) => {
                    this.modules = response.data;
                    if (response.data.length != 0) {
                        this.selected_module_id = response.data[0].id;
                        this.getTestcaseByModuleID(this.selected_module_id);
                    } else {
                        this.selected_module_id = null;
                        this.unselected = null;
                    }
                })
                .catch((error) => {
                    that.$message.error('服务器错误');
                });
            this.switchVisible = false;
            this.selected_testcase = [];
        },
        switchProject() {
            if (this.selected_testcase.length != 0) {
                this.switchVisible = true;
            } else {
                this.getModulesByProjectID(this.selected_project_id);
            }
        },

        saveEdit() {
            this.changeResult();
            let datas = {
                name: this.name,
                project_id: this.selected_project_id,
                include: this.include,
                tester: this.tester,
                desc: this.desc
            };
            update_locust(this.current_locust_id, datas)
                .then((response) => {
                    this.$message.success('修改成功！');
                    this.editVisible = false;
                    this.close_page();
                })
                .catch((error) => {
                    if (typeof error === 'object') {
                        let error_str = '';
                        for (let key in error) {
                            let err = error[key];
                            error_str = error_str + key + ':' + err[0] + ' \n ';
                        }
                        this.$message.error(error_str);
                    } else {
                        // console.log(error);
                        this.$message.error('服务器错误');
                    }
                });
        },
        clearValidate(prop_value) {
            this.$refs['form'].clearValidate(prop_value);
        },
        resetForm(formName) {
            this.$refs[formName].resetFields(); // 清空表单
        },
        getProjectNames() {
            projects_names()
                .then((response) => {
                    this.project_names = response.data;
                })
                .catch((error) => {
                    that.$message.error('服务器错误');
                });
        },
        removeHandle(event) {
            console.log(event);
            this.$message.success(`从 ${event.from.id} 移动到 ${event.to.id} `);
        },
        changeResult() {
            var len = this.selected_testcase.length;
            var text = '[';
            for (var i = 0; i < len; i++) {
                if (i === len - 1) {
                    text += this.selected_testcase[i].id + ']';
                } else {
                    text += this.selected_testcase[i].id + ', ';
                }
            }
            if (len === 0) {
                text = '[]';
            }
            this.include = text;
        },
        getTestcaseByModuleID(choose_selected_module_id) {
            testcases_by_module_id(choose_selected_module_id)
                .then((response) => {
                    this.unselected = response.data;
                    if (this.selected_testcase.length != 0) {
                        this.selected_testcase.forEach((element) => {
                            this.unselected = this.unselected.filter((item) => {
                                return item.id !== element.id;
                            });
                        });
                    }
                })
                .catch((error) => {
                    that.$message.error('服务器错误');
                });
        },
        getLocustDetail() {
            get_detail_locust(this.current_locust_id)
                .then((response) => {
                    this.name = response.data.name;
                    this.selected_project_id = response.data.project_id;
                    this.getModulesByProjectID(this.selected_project_id);
                    this.selected_testcase = response.data.include;
                    this.tester = response.data.tester;
                    this.desc = response.data.desc;
                })
                .catch((error) => {
                    this.$message.error('服务器错误');
                });
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
    /*height: 500px;*/
    height: 400px;
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
</style>
