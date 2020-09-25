<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-calendar"></i> 模块管理
                </el-breadcrumb-item>
                <el-breadcrumb-item>新增模块</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <div class="form-box">
                <el-form ref="form" :rules="rules" :model="form" label-width="100px">
                    <el-form-item label="模块名称" prop="name" required>
                        <el-input
                            v-model="form.name"
                            suffix-icon="el-icon-menu"
                            @focus="clearValidate('name')"
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

                    <el-form-item label="所属项目" prop="project_id" required>
                        <el-select v-model="form.project_id" placeholder="请选择">
                            <!-- <el-option key="bbk" label="项目1" value="1"></el-option>
                            <el-option key="xtc" label="项目2" value="2"></el-option>
                            <el-option key="imoo" label="项目3" value="3"></el-option>-->
                            <el-option
                                v-for="(item, key) in project_names"
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
import { add_module, projects_names } from '../../api/api';
import bus from '../common/bus';

export default {
    name: 'baseform',
    data: function () {
        return {
            form: {
                name: '', // 模块名称
                tester: '', // 测试人员
                project_id: '', // 项目ID
                desc: '' // 简要描述
            },
            rules: {
                name: [{ required: true, message: '请输入模块名称', trigger: 'blur' }],
                tester: [{ required: true, message: '请输入测试人员', trigger: 'blur' }],
                project_id: [{ required: true, message: '请选择所属项目', trigger: 'blur' }]
            },
            project_names: []
        };
    },
    created() {
        this.getProjectNames();
    },
    methods: {
        close_page() {
            this.$refs['form'].resetFields();
            this.$router.go(-1);
            bus.$emit('close_current_tags');
        },
        onSubmit(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    let that = this;
                    add_module(this.form)
                        .then((response) => {
                            this.$message.success('新增模块成功！');
                            this.close_page();
                        })
                        .catch((error) => {
                            if (typeof error === 'object' && error.hasOwnProperty('name')) {
                                // this.$message.error(error.name[0]);
                                this.$message.error('模块名称已存在');
                            } else {
                                console.log(error);
                                this.$message.error('服务器错误');
                            }
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