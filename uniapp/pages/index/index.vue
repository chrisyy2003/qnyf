<template>
	<view style="padding: 15px 15px 40px 15px;">
		<u-toast ref="uToast"></u-toast>
		<uni-card title="✅✅ 青柠打卡说明">
			<u--text text="1.填入基本信息即可每日自动打卡"></u--text>
			<u--text text="2.如果需要更新信息（例如密码，打卡位置）只重新填入一次即可"></u--text>
			<u--text text="3.输入学号和学校可查看当前打卡状态"></u--text>
			<u--text text="4.输入学号和学校即可删除打卡信息,并停止打卡"></u--text>
			<u-divider></u-divider>
			<u-text :text="'⭐目前已有' + count + '位同学正在自动打卡！'" color="#826a9a"></u-text>
			<u-text text="🤡如果发现没有打卡成功，请检查自己的打卡状态" color="#826a9a"></u-text>
			<u-text text="☔此qq可以审批出入申请，请咨询" color="#826a9a"></u-text>
			<u-link href="https://tool.gljlw.com/qqq/?qq=3534328609" text="QQ:3534328609" :under-line="true"></u-link>
			<u-text text="✔此项目开源，仓库地址：" color="#826a9a"></u-text>
			<u-link href="https://github.com/chrisyang2003/qnyf" text="chrisyang2003/qnyf" :under-line="true"></u-link>
			
		</uni-card>
		<u--form labelPosition="left" :model="form" style="padding-left: 30rpx; padding-right: 30rpx;">
			<u-form-item label="学校" prop="userInfo.name">
				<u-picker keyName="name" :show="show" :columns="columns" @cancel="form.school = ''; show = false"
					@confirm="confirm"></u-picker>
				<!-- <u--input v-model="form.school" border="surround"></u--input> -->
				<u-button @click="show = true">{{form.school ? form.school : "请选择学校"}}</u-button>
			</u-form-item>

			<u-form-item label="学号">
				<u--input v-model="form.num" border="surround" placeholder="请输入学号" inputAlign="center"></u--input>
			</u-form-item>

			<u-form-item label="姓名">
				<u--input v-model="form.name" border="surround" placeholder="请输入姓名" inputAlign="center"></u--input>
			</u-form-item>

			<u-form-item label="密码">
				<u--input v-model="form.passwd" border="surround" placeholder="请输入密码" inputAlign="center"></u--input>
			</u-form-item>

			<u-form-item label="位置">
				<u-button @click="chooseLocation">{{hasLocation? form.address : '点击选择打卡地址'}}</u-button>
			</u-form-item>
		</u--form>

		<!-- <map style="width: 100%; height: 300px;" :latitude="latitude" :longitude="longitude"></map> -->
		<u-gap></u-gap>
		<u-row gutter="10">
			<u-col span="4">
				<u-button text="提交信息" type="primary" @click="submit"></u-button>
			</u-col>
			<u-col span="4">
				<u-button text="查询打卡状态" type="info" @click="query"></u-button>
			</u-col>
			<u-col span="4">
				<u-button text="停止打卡" type="error" @click="stop"></u-button>
			</u-col>
		</u-row>

	</view>
</template>

<script>
	export default {
		onLoad() {
			this.$api.dakacount().then(res => {
				this.count = res.data
			})

		},
		data() {
			return {
				hasLocation: false,
				show: false,
				columns: [
					[{
							name: '西华大学',
							value: '10623'
						},
						{
							name: '成都银杏酒店管理学院',
							value: '13670'
						}
					]
				],
				form: {
					name: '',
					school: '',
					passwd: '',
					num: '',
					yxdm: '',
					address: ''
				},
				count: 0,

				address: ''

			};
		},
		methods: {
			chooseLocation() {

				
				uni.chooseLocation({
					success: (res) => {
						this.hasLocation = true
						this.form.address = res.address

						console.log('位置名称：' + res.name);
						console.log('详细地址：' + res.address);
					}
				})
			},
			confirm(e) {
				console.log(e)
				this.show = false
				this.form.school = e.value[0].name
				this.form.yxdm = e.value[0].value
			},

			submit() {
				console.log(this.form)

				if (!this.form.name || !this.form.num || !this.form.passwd || !this.form.school || !this.form.yxdm || !this
					.form.address) {
					uni.showToast({
						title: "信息不完整",
						icon: "error",
						duration: 2000
					})
					return
				}

				this.$api.submit(this.form).then(res => {
					if (res.code == 200) {
						uni.showToast({
							title: res.msg,
							icon: "success",
							duration: 2000
						})
					}
				})


			},
			query() {
				if (!this.form.num || !this.form.yxdm) {
					uni.showToast({
						title: "信息不完整",
						icon: "error",
						duration: 2000
					})
					return
				}
				
				this.$api.query(this.form).then(res => {
					if (res.code == 200){
						this.$refs.uToast.show({
							duration: 5000,
							type: 'success',
							position: "top",
							message: res.msg,
							iconUrl: 'https://cdn.uviewui.com/uview/demo/toast/success.png'
						
						})
					}
					
					console.log(res)
				})


			},
			stop() {
				if (!this.form.num || !this.form.yxdm) {
					uni.showToast({
						title: "信息不完整",
						icon: "error",
						duration: 2000
					})
					return
				}
				
				this.$api.stop(this.form).then(res => {
					if (res.code == 200){
						uni.showToast({
							title: res.msg,
							icon: "success",
							duration: 2000
						})
					}
				})
				
			},
		},
	};
</script>
