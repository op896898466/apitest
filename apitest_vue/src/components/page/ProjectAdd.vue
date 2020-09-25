<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-calendar"></i> 项目管理
                </el-breadcrumb-item>
                <el-breadcrumb-item>新增项目</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <div class="form-box">
                <el-form ref="form" :rules="rules" :model="form" label-width="100px">
                    <el-form-item label="项目名称" prop="name" required>
                        <el-input
                            v-model="form.name"
                            suffix-icon="el-icon-menu"
                            @focus="clearValidate('name')"
                            clearable
                        ></el-input>
                    </el-form-item>

                    <el-form-item label="负责人" prop="leader" required>
                        <el-input
                            v-model="form.leader"
                            suffix-icon="el-icon-s-custom"
                            @focus="clearValidate('leader')"
                            clearable
                        ></el-input>
                    </el-form-item>

                    <el-form-item label="测试人员" prop="tester" required>
                        <el-input
                            v-model="form.tester"
                            suffix-icon="el-icon-user-solid"
                            @focus="clearValidate('tester')"
                            clearable
                        ></el-input>
                    </el-form-item>

                    <el-form-item label="开发人员" prop="programmer" required>
                        <el-input
                            v-model="form.programmer"
                            suffix-icon="el-icon-user-solid"
                            @focus="clearValidate('programmer')"
                            clearable
                        ></el-input>
                    </el-form-item>

                    <el-form-item label="发布应用" prop="publish_app" required>
                        <el-input
                            v-model="form.publish_app"
                            suffix-icon="el-icon-s-promotion"
                            @focus="clearValidate('publish_app')"
                            clearable
                        ></el-input>
                    </el-form-item>

                    <el-form-item label="内置函数" prop="debugtalk_id">
                        <el-select
                            v-model="form.debugtalk_id"
                            clearable
                            placeholder="请选择"
                            style="width:100%"
                        >
                            <el-option
                                v-for="(item, key) in debugtalk_names"
                                :key="key"
                                :label="item.name"
                                :value="item.id"
                            ></el-option>
                        </el-select>
                    </el-form-item>

                    <el-form-item label="简要描述" prop="desc">
                        <el-input type="textarea" rows="4" v-model="form.desc" clearable></el-input>
                    </el-form-item>

                    <el-form-item>
                        <el-button type="primary" @click="onSubmit('form')">提交</el-button>
                        <el-button @click="close_page()">取消</el-button>
                    </el-form-item>
                </el-form>
            </div>
        </div>
    </div>
</template>

<script>
import { add_project, projects_names, builtins_names } from '../../api/api';
import bus from '../common/bus';

export default {
    name: 'baseform',
    data: function () {
        var validateName = (rule, value, callback) => {
            var len = value.length;
            if (len <= 0) {
                callback(new Error('请输入项目名称'));
            } else {
                for (let index = 0; index < this.project_names.length; index++) {
                    var element = this.project_names[index];
                    if (element.name === value) {
                        // alert(element.name);
                        callback(new Error('项目名称已存在'));
                        break;
                    }
                }
                callback();
            }
        };
        return {
            form: {
                name: '', // 项目名称
                leader: '', // 项目负责人
                tester: '', // 项目测试人员
                programmer: '', // 开发人员
                publish_app: '', // 发布应用
                desc: '', // 简要描述
                debugtalk_id: ''
            },
            rules: {
                name: [{ validator: validateName, trigger: 'blur' }],
                leader: [{ required: true, message: '请输入项目负责人', trigger: 'blur' }],
                tester: [{ required: true, message: '请输入测试人员', trigger: 'blur' }],
                programmer: [{ required: true, message: '请输入开发人员', trigger: 'blur' }],
                publish_app: [{ required: true, message: '请输入发布应用', trigger: 'blur' }]
            },
            project_names: [],
            debugtalk_names: []
        };
    },
    created() {
        this.getProjectNames();
        this.getDebugTalks();
    },
    methods: {
        close_page() {
            this.$refs['form'].resetFields();
            this.$router.go(-1);
            bus.$emit('close_current_tags');
        },
        getDebugTalks() {
            builtins_names()
                .then((response) => {
                    this.debugtalk_names = response.data;
                })
                .catch((error) => {
                    that.$message.error('服务器错误');
                });
        },
        onSubmit(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    if (!this.form.debugtalk_id) {
                        delete this.form.debugtalk_id;
                    }
                    add_project(this.form)
                        .then((response) => {
                            this.$message.success('新增项目成功！');
                            this.close_page();
                        })
                        .catch((error) => {
                            console.log(error);
                            this.$message.error('服务器错误');
                        });
                } else {
                    this.$message.error('参数有误');
                    return false;
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
        }
    }
};
</script>

<style scoped>
/* .el-select .el-input__inner {


        width: 300px;

} */
</style>