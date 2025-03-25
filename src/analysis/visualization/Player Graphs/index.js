import puppeteer from 'puppeteer-core';

async function run() {
	let browser;
	try {
		const auth = 'brd-customer-hl_64e0b759-zone-zone1:2gt7rkygpnlq';

		browser = await puppeteer.connect({
			browserWSEndpoint: `wss://${auth}@zproxy.lum-superproxy.io:9222`,
		});

		console.log('hello');
		const page = await browser.newPage();
		page.setDefaultNavigationTimeout(2 * 60 * 1000);

		await page.goto('https://www.espn.com/mlb/stats/player');

		const productsData = await page.evaluate(() => {
			const products = Array.from(document.querySelectorAll('.a-carousel'));
			return products.map((product) => {
				const titleElement = product.querySelector(
					'.p13n-sc-truncate-desktop-type2'
				);
				const priceElement = product.querySelector('.p13n-sc-price');

				return {
					title: titleElement ? titleElement.innerText.trim() : null,
					price: priceElement ? priceElement.innerText.trim() : null,
				};
			});
		});

		console.log(productsData);
	} catch (e) {
		console.error('scrape failed', e);
	} finally {
		await browser?.close();
	}
}

//This is and update just before june, this is so much fun

await run();
