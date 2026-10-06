# Image OCR Feature for MBTI Personality Analyzer

## ✨ New Feature: Image Text Recognition

The app now supports uploading images containing text! The app will extract text using Optical Character Recognition (OCR) and analyze it for MBTI personality prediction.

## 📦 Installation

To use the new image OCR feature, install the required dependencies:

```bash
pip install -r requirements.txt
```

This will install:
- `easyocr>=1.7` - For OCR text extraction
- `pillow>=10.0` - For image processing

**Note:** On first run, EasyOCR will download language models (~100MB). This happens automatically on first use.

## 🚀 How to Use

### Method 1: In the Main App (`app.py`)
1. Run the app: `streamlit run app.py`
2. In the sidebar, select "🖼️ Image (OCR)" as the input method
3. Upload an image file (PNG, JPG, or JPEG)
4. The app will automatically extract text from the image
5. Click "Analyze ✨" to get MBTI predictions

### Method 2: In the Analysis Page (`pages/2_Analysis.py`)
1. Navigate to the Analysis page
2. Select "🖼️ Image Upload (OCR)" option
3. Upload your image
4. View the extracted text
5. Click "🔮 Analyze Text" for predictions

## 📝 What It Does

1. **Image Upload**: Upload images containing text (screenshots, photos, memes, etc.)
2. **OCR Processing**: Automatically extracts all visible text from the image
3. **Text Analysis**: Uses the extracted text for MBTI personality prediction
4. **Full Feature Set**: All existing features work with OCR-extracted text:
   - MBTI personality prediction
   - Emotion analysis
   - Sentiment analysis
   - Gauge visualizations
   - Multi-model ensemble predictions

## 🎯 Supported Image Types

- **Formats**: PNG, JPG, JPEG
- **Content**: Any image containing readable text:
  - Screenshots of social media posts
  - Images with quotes or comments
  - Photos of handwritten or printed text
  - Memes with text overlays

## 💡 Tips for Best Results

1. **Clear Images**: Upload high-quality, clear images for better OCR accuracy
2. **Readable Text**: Ensure text is clearly visible and not blurry
3. **Good Lighting**: Images with good contrast work better
4. **Straight Text**: Photos with text at angles may have reduced accuracy

## 🔧 Technical Details

- **OCR Engine**: EasyOCR (supports 80+ languages, including English)
- **Processing**: Uses GPU acceleration if available (falls back to CPU)
- **Caching**: OCR reader is cached for performance on subsequent uses
- **Error Handling**: Gracefully handles images with no extractable text

## 📊 Example Use Cases

1. **Social Media Analysis**: Upload screenshots of posts/comments to analyze personality
2. **Text in Images**: Analyze personality from text overlays in images
3. **Handwritten Text**: Upload photos of handwritten text (if clear enough)
4. **Batch Processing**: Use in Analysis page for batch predictions from multiple images

## ⚙️ Configuration

The OCR feature can be customized in `ocr_utils.py`:
- Language support: Currently set to English (`'en'`)
- GPU usage: Set `gpu=True` in `get_ocr_reader()` if you have GPU support
- Additional languages: Add language codes in the `easyocr.Reader(['en'])` list

## 🐛 Troubleshooting

**Issue**: OCR is slow
- **Solution**: First-time use downloads models (~100MB). Subsequent uses are faster.

**Issue**: No text extracted
- **Solution**: Ensure image has clear, readable text. Try a different image.

**Issue**: Installation errors
- **Solution**: On some systems, you may need to install additional dependencies:
  ```bash
  pip install torch torchvision
  ```

## 📦 Files Added/Modified

- ✅ `requirements.txt` - Added easyocr and pillow
- ✅ `ocr_utils.py` - New OCR utility functions
- ✅ `app.py` - Added image upload UI in main app
- ✅ `pages/2_Analysis.py` - Added image upload UI in analysis page

Enjoy analyzing MBTI personality from images! 🎉

