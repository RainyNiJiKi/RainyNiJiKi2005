# Low-poly Face Mask AR

หน้ากากทรงเหลี่ยมตามภาพตัวอย่าง: หัวทรงสี่เหลี่ยมตัดมุมด้านบน คิ้วแดงเข้ม ตาสีม่วงเทา รูม่านตาสี่เหลี่ยมสีดำ และปากแดงสองชั้น

## ไฟล์
- `blender_face_mask.py`: สร้างโมเดลใน Blender และส่งออก `face_mask_ar.glb`
- `face_ar.html`: เว็บติดตามใบหน้าด้วย MindAR
- `face_mask_ar.glb`: ต้องสร้างด้วย Blender แล้วอัปโหลดไว้ข้าง HTML

## วิธีใช้
1. เปิด Blender > Scripting แล้วเปิด `blender_face_mask.py`
2. กด Run Script เพื่อส่งออก GLB
3. อัปโหลด `face_mask_ar.glb` ไปยังโฟลเดอร์เดียวกับ `face_ar.html` ใน repository
4. เปิดผ่าน GitHub Pages/HTTPS และอนุญาตกล้อง
5. ใช้ปุ่มบนจอปรับขนาดและตำแหน่งได้

หมายเหตุ: ต้องทดสอบบนอุปกรณ์จริงเพื่อปรับแนวและขนาดให้ตรงกับใบหน้า
