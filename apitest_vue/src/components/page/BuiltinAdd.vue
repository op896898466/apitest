<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-calendar"></i> 函数管理
                </el-breadcrumb-item>
                <el-breadcrumb-item>新增函数</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-form ref="form" :model="form" label-width="100px">
                <el-form-item label="函数名称" m prop="name" required>
                    <el-input v-model="form.name" suffix-icon="el-icon-menu" clearable></el-input>
                </el-form-item>

                <el-form-item label="函数内容" prop="debugtalk" required>
                    <editor
                        style="font-size: 15px"
                        v-model="form.debugtalk"
                        @init="editorInit"
                        lang="python"
                        theme="monokai"
                        width="100%"
                        height="600px"
                        :options="{
                                enableSnippets:true,
                                enableBasicAutocompletion: true,
                                enableLiveAutocompletion: true
                            }"
                    ></editor>
                </el-form-item>
                <el-form-item>
                    <el-button
                        type="primary"
                        size="medium"
                        style="margin-right: 10px;"
                        @click="onSubmit('form')"
                    >提交</el-button>
                    <el-button type="danger" size="medium" @click="close_page()">取消</el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>

<script>
import { add_builtin } from '../../api/api';
import bus from '../common/bus';

export default {
    // beforeRouteLeave (to, from, next) {
    //     // 页面离开切换到其他组件之间被调用
    //     console.log("before route leave")
    //     next()
    // },
    // props: ['id'],
    components: {
        editor: require('vue2-ace-editor')
    },
    name: 'basetable',
    data() {
        return {
            form: {
                name: '',
                debugtalk: '#debugtalk.py'
            }
        };
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
                    add_builtin(this.form)
                        .then((response) => {
                            this.$message.success('新函数成功！');    
                            this.close_page();
     
                        })
                        .catch((error) => {
                            if (typeof error === 'object' && error.hasOwnProperty('name')) {
                                this.$message.error('函数名称已存在');
                            } else {
                                // console.log(error);
                                this.$message.error('服务器错误');
                            }
                        });
                } else {
                    this.$message.error('参数有误');
                    return false;
                }
            });
        },
        editorInit() {
            require('brace/ext/language_tools');
            require('brace/mode/python');
            require('brace/theme/monokai');
            require('brace/snippets/python');
        }
        // 更新指定的内置函数源码

        // 返回函数列表页
    }
    // mounted() {
    //     this.getCode();
    // },
    // created() {
    //     this.getCode();
    // },
};
</script>
