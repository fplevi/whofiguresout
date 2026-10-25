// Captures the case evidence from the published prototype. Usage: node capture-all.mjs
import { createRequire } from 'module';
const require = createRequire('D:/Projetos/BurguerKingNewSite/prototype/package.json');
const { chromium } = require('@playwright/test');
const out = 'D:/Projetos/Portfolio/.scratch/burger-king/captures/';
const base = 'https://fplevi.github.io/BurguerKingDelivery/';
const browser = await chromium.launch({ channel: 'chrome' });

async function run(name, viewport, flow) {
  const page = await browser.newPage({ viewport, deviceScaleFactor: viewport.width < 500 ? 2 : 1 });
  const shot = async (n, opts = {}) => {
    await page.waitForTimeout(1200);
    await page.evaluate(() => document.activeElement?.blur());
    await page.screenshot({ path: `${out}${name}-${n}.png`, ...opts });
    console.log(name, n, page.url());
  };
  await page.goto(base); await page.waitForTimeout(4500);
  await flow(page, shot);
  await page.close();
}

const removeCheese = async (page) => {
  await page.locator('section.hero').getByRole('button', { name: /Ver ingredientes/ }).click();
  await page.waitForTimeout(1500);
  await page.locator('#controls').getByRole('button', { name: /Queijo/ }).first().click();
  await page.waitForTimeout(800);
};

await run('desktop', { width: 1440, height: 1000 }, async (page, shot) => {
  await shot('menu');
  await removeCheese(page);
  await shot('ingredients-removed');
  await page.locator('#apply').click();
  await page.locator('section.hero').getByRole('button', { name: 'Adicionar ao carrinho' }).click();
  await page.getByRole('banner').getByRole('button', { name: /^Carrinho · / }).click();
  await page.waitForTimeout(6000); // let the toast go
  await shot('cart');
  await page.getByRole('button', { name: 'Continuar' }).click();
  await page.getByRole('textbox', { name: /Celular/ }).fill('61999991234');
  await page.getByRole('button', { name: /WhatsApp/ }).click();
  await page.getByRole('textbox', { name: /Código/ }).fill('123456');
  await page.getByRole('button', { name: 'Confirmar e continuar' }).click();
  await page.waitForTimeout(800);
  await page.getByRole('button', { name: 'Entregar neste endereço' }).click();
  await page.waitForTimeout(800);
  await page.getByText('Pix', { exact: true }).first().click();
  await page.evaluate(() => window.scrollTo(0, 0));
  await shot('checkout');
  await page.getByText('Cartão de crédito', { exact: true }).first().click();
  await page.getByRole('textbox', { name: /segurança/i }).first().fill('123');
  await page.getByRole('button', { name: /Confirmar e pagar/ }).first().click();
  await page.waitForTimeout(2500);
  await page.getByRole('button', { name: 'Acompanhar pedido' }).click();
  await page.waitForTimeout(90000); // let the order advance a status or two
  await page.evaluate(() => window.scrollTo(0, 0));
  await shot('tracking');
});

await run('mobile', { width: 390, height: 844 }, async (page, shot) => {
  await shot('menu');
  await removeCheese(page);
  await shot('ingredients');
});
await browser.close();
