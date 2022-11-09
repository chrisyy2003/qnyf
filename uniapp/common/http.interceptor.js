// 这里的vm，就是我们在vue文件里面的this，所以我们能在这里获取vuex的变量，比如存放在里面的token
// 同时，我们也可以在此使用getApp().globalData，如果你把token放在getApp().globalData的话，也是可以使用的
module.exports = (vm) => {
	// 初始化请求配置
	uni.$u.http.setConfig((config) => {
		/* config 为默认全局配置*/
		// config.baseURL = 'http://chrisyy.top:4000'; /* 根域名 */
		config.loadingText = '努力加载中~';
		return config
	})


	uni.$u.http.interceptors.response.use((res) => {

		const result = res.data
		switch (result.code) {
			case 400:
				uni.showToast({
					title: result.msg,
					icon: "error",
					duration: 3500
				})
				return result
			case 500:
				uni.showToast({
					title: result.msg,
					icon: "error",
					duration: 3500
				})
				return result
		}
		return result
	})
}
