import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('http://192.168.1.17:3000/');
  await page.locator('input[type="file"]').click();
  await page.locator('input[type="file"]').setInputFiles('File.pdf');
  await page.getByRole('button', { name: 'Uploadcloud_upload' }).click();
});