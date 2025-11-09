"""
Panasonic Lunch Navi (パナラン)
社内ランチ情報共有アプリケーション
"""

import streamlit as st
import json
from datetime import datetime
import os

# ページ設定
st.set_page_config(
    page_title="パナラン - Panasonic Lunch Navi",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# セッション状態の初期化
if 'stores' not in st.session_state:
    st.session_state.stores = []
if 'show_success' not in st.session_state:
    st.session_state.show_success = False
if 'success_message' not in st.session_state:
    st.session_state.success_message = ""
if 'sort_order' not in st.session_state:
    st.session_state.sort_order = "登録日（新しい順）"
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'show_balloons' not in st.session_state:
    st.session_state.show_balloons = False

# データファイルのパス
STORES_FILE = "stores.json"

def load_stores():
    """店舗データをJSONファイルから読み込む"""
    if os.path.exists(STORES_FILE):
        try:
            with open(STORES_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                stores = data.get("stores", [])
                # セッション状態を更新
                st.session_state.stores = stores
                return stores
        except (json.JSONDecodeError, FileNotFoundError):
            st.session_state.stores = []
            return []
    st.session_state.stores = []
    return []

def save_stores(stores, rerun=True):
    """店舗データをJSONファイルに保存する"""
    data = {"stores": stores}
    with open(STORES_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    # セッション状態を更新
    st.session_state.stores = stores
    # 自動リロードのトリガー（必要に応じて）
    if rerun:
        st.rerun()

def filter_stores(stores, keyword="", genre="", max_price=None):
    """店舗をキーワード、ジャンル、価格でフィルタリング"""
    filtered = stores
    
    if keyword:
        filtered = [s for s in filtered if keyword.lower() in s.get("name", "").lower()]
    
    if genre:
        filtered = [s for s in filtered if s.get("genre") == genre]
    
    if max_price:
        filtered = [s for s in filtered if s.get("price", 0) <= max_price]
    
    return filtered

def sort_stores(stores, sort_order):
    """店舗を並び替える"""
    if sort_order == "評価（高い順）":
        return sorted(stores, key=lambda x: calculate_rating(x.get('reviews', [])), reverse=True)
    elif sort_order == "評価（低い順）":
        return sorted(stores, key=lambda x: calculate_rating(x.get('reviews', [])), reverse=False)
    elif sort_order == "価格（安い順）":
        return sorted(stores, key=lambda x: x.get('price', 0))
    elif sort_order == "価格（高い順）":
        return sorted(stores, key=lambda x: x.get('price', 0), reverse=True)
    elif sort_order == "登録日（新しい順）":
        return sorted(stores, key=lambda x: x.get('posted_date', ''), reverse=True)
    elif sort_order == "登録日（古い順）":
        return sorted(stores, key=lambda x: x.get('posted_date', ''), reverse=False)
    return stores

def calculate_rating(reviews):
    """レビューから平均評価を計算"""
    if not reviews:
        return 0.0
    total = sum(r.get("rating", 0) for r in reviews)
    return round(total / len(reviews), 1)

def display_rating(rating, size="large"):
    """評価を星で表示"""
    full_stars = int(rating)
    half_star = 1 if rating - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    
    stars = "⭐" * full_stars
    if half_star:
        stars += "⭐"
    stars += "☆" * empty_stars
    
    if size == "large":
        return f"<h3>{stars} {rating:.1f}</h3>"
    else:
        return f"{stars} {rating:.1f}"

# ダークモード/ホワイトモード切り替え（FB-1対応）
def get_theme_css(dark_mode):
    """テーマに応じたCSSを返す"""
    if dark_mode:
        return """
        <style>
            .main-title {
                font-size: 2.5rem;
                font-weight: bold;
                text-align: center;
                margin-bottom: 1rem;
                cursor: pointer;
                color: #ffffff;
            }
            .main-title:hover {
                color: #FF6B6B;
            }
            .store-card {
                border: 2px solid #444;
                border-radius: 10px;
                padding: 1rem;
                margin: 1rem 0;
                background-color: #2d2d2d;
                color: #ffffff;
            }
            .rating-large {
                font-size: 1.5rem;
                color: #FFD700;
            }
            .review-section {
                margin-top: 1rem;
                padding-top: 1rem;
                border-top: 2px solid #444;
            }
            .stButton>button {
                width: 100%;
            }
            .stMarkdown {
                color: #ffffff;
            }
        </style>
        """
    else:
        return """
        <style>
            .main-title {
                font-size: 2.5rem;
                font-weight: bold;
                text-align: center;
                margin-bottom: 1rem;
                cursor: pointer;
            }
            .main-title:hover {
                color: #FF6B6B;
            }
            .store-card {
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                padding: 1rem;
                margin: 1rem 0;
                background-color: #f9f9f9;
            }
            .rating-large {
                font-size: 1.5rem;
                color: #FFD700;
            }
            .review-section {
                margin-top: 1rem;
                padding-top: 1rem;
                border-top: 2px solid #e0e0e0;
            }
            .stButton>button {
                width: 100%;
            }
        </style>
        """

# カスタムCSS適用
st.markdown(get_theme_css(st.session_state.dark_mode), unsafe_allow_html=True)

# メインタイトル（クリックでリロード）
col_title, col_refresh = st.columns([5, 1])
with col_title:
    if st.button("🍽️ **Panasonic Lunch Navi（パナラン）**", key="title_button", help="クリックでホームに戻る"):
        st.rerun()
with col_refresh:
    if st.button("🔄", help="ページをリロード"):
        st.rerun()

st.markdown("---")

# データ読み込み
stores = load_stores()

# サイドバー: 検索・フィルター・並び替え
with st.sidebar:
    # ダークモード/ホワイトモード切り替え（FB-1対応）
    st.header("🎨 表示設定")
    dark_mode = st.toggle("🌙 ダークモード", value=st.session_state.dark_mode, help="ダークモード/ホワイトモードを切り替えます")
    if dark_mode != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_mode
        st.rerun()
    
    st.markdown("---")
    st.header("🔍 検索・フィルター")
    
    # キーワード検索
    keyword = st.text_input("店舗名で検索", "", help="店舗名の一部を入力して検索できます")
    
    # ジャンルフィルター
    genres = ["すべて"] + sorted(list(set(s.get("genre", "") for s in stores if s.get("genre"))))
    selected_genre = st.selectbox("ジャンル", genres, help="ジャンルで絞り込むことができます")
    genre_filter = "" if selected_genre == "すべて" else selected_genre
    
    # 価格フィルター
    max_price = st.slider("最大価格", 0, 2000, 2000, step=100, help="この価格以下の店舗を表示します")
    
    st.markdown("---")
    st.header("📊 並び替え")
    
    # 並び替えオプション（FB-8対応）
    sort_options = [
        "登録日（新しい順）",
        "登録日（古い順）",
        "評価（高い順）",
        "評価（低い順）",
        "価格（安い順）",
        "価格（高い順）"
    ]
    st.session_state.sort_order = st.selectbox(
        "並び替え", 
        sort_options,
        index=sort_options.index(st.session_state.sort_order) if st.session_state.sort_order in sort_options else 0,
        help="店舗の並び順を変更できます"
    )
    
    st.markdown("---")
    st.markdown("### 📊 統計")
    st.write(f"**登録店舗数**: {len(stores)}件")
    
    filtered_count = len(filter_stores(stores, keyword, genre_filter, max_price))
    st.write(f"**表示件数**: {filtered_count}件")

# タブを作成
tab1, tab2, tab3 = st.tabs(["🏪 店舗一覧", "➕ 新規投稿", "💬 レビュー投稿"])

# タブ1: 店舗一覧
with tab1:
    st.header("店舗一覧")
    
    if not stores:
        st.info("📝 まだ店舗が登録されていません。新規投稿タブから店舗を追加してください。")
    else:
        # フィルタリング
        filtered_stores = filter_stores(stores, keyword, genre_filter, max_price)
        
        # 並び替え（FB-8対応）
        filtered_stores = sort_stores(filtered_stores, st.session_state.sort_order)
        
        if not filtered_stores:
            st.warning("🔍 該当する店舗がありません。検索条件を変更してください。")
        else:
            # 店舗をカード形式で表示
            for store in filtered_stores:
                # 評価を計算
                reviews = store.get('reviews', [])
                rating = calculate_rating(reviews)
                
                # 店舗カード
                with st.container():
                    st.markdown(f"""
                    <div class="store-card">
                        <h2>🍽️ {store.get('name', '不明')}</h2>
                        <p><strong>ジャンル:</strong> {store.get('genre', '未設定')} | 
                        <strong>価格:</strong> 💰{store.get('price', 0)}円</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 評価表示（FB-12対応：大きく表示）
                    if rating > 0:
                        st.markdown(f"""
                        <div class="rating-large">
                            {display_rating(rating, "large")}
                            <p>レビュー数: {len(reviews)}件</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.info("⭐ レビューはまだありません")
                    
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.write(f"**📍 場所**: {store.get('location', '未設定')}")
                        st.write(f"**👤 投稿者**: {store.get('posted_by', '不明')}")
                        st.write(f"**📅 投稿日**: {store.get('posted_date', '不明')}")
                    
                    # レビュー表示（FB-14対応：店舗情報と統合）
                    if reviews:
                        st.markdown("---")
                        st.markdown("### 💬 レビュー")
                        for i, review in enumerate(reviews):
                            with st.expander(f"⭐{review.get('rating', 0)} - {review.get('user', '不明')} ({review.get('date', '不明')})"):
                                st.write(review.get('comment', ''))
                    
                    st.markdown("---")

# タブ2: 新規投稿
with tab2:
    st.header("➕ 新規店舗投稿")
    st.info("💡 新しいランチ店を投稿できます。必須項目（*）を入力してください。")
    
    with st.form("new_store_form", clear_on_submit=True):
        user_name = st.text_input("👤 ユーザー名（メールアドレスまたは表示名）*", "", help="投稿者名を入力してください")
        store_name = st.text_input("🍽️ 店舗名*", "", help="店舗の名前を入力してください")
        genre = st.selectbox("🍱 ジャンル*", ["和食", "洋食", "中華", "イタリアン", "カフェ", "その他"], help="店舗のジャンルを選択してください")
        price = st.number_input("💰 価格（円）*", min_value=0, max_value=5000, value=1000, step=100, help="ランチの価格を入力してください")
        location = st.text_input("📍 場所（例: 大阪本社から徒歩5分）*", "", help="店舗の場所を入力してください")
        
        submitted = st.form_submit_button("📝 投稿する", use_container_width=True)
        
        if submitted:
            if user_name and store_name and location:
                # 新しい店舗IDを生成
                existing_ids = [int(s.get('id', 'store000').replace('store', '')) for s in stores if s.get('id', '').startswith('store')]
                new_id_num = max(existing_ids) + 1 if existing_ids else 1
                new_id = f"store{new_id_num:03d}"
                
                # 新しい店舗データ
                new_store = {
                    "id": new_id,
                    "name": store_name,
                    "genre": genre,
                    "price": price,
                    "location": location,
                    "rating": 0.0,
                    "reviews": [],
                    "posted_by": user_name,
                    "posted_date": datetime.now().strftime("%Y-%m-%d")
                }
                
                # データに追加
                stores.append(new_store)
                save_stores(stores, rerun=False)
                
                # 成功メッセージ（FB-5対応：一度だけ表示）
                st.session_state.show_success = True
                st.session_state.success_message = f"✅ {store_name} を投稿しました！"
                st.session_state.show_balloons = True
                
                # リロードして反映（FB-2, FB-4対応）
                st.rerun()
            else:
                st.error("⚠️ 必須項目（*）を入力してください。")

# タブ3: レビュー投稿
with tab3:
    st.header("💬 レビュー投稿")
    st.info("💡 店舗にレビューを投稿できます。必須項目（*）を入力してください。")
    
    if not stores:
        st.warning("📝 まず店舗を投稿してください。")
    else:
        # 店舗選択
        store_options = {f"{s.get('name')} ({s.get('genre')})": s.get('id') for s in stores}
        selected_store_name = st.selectbox("🍽️ 店舗を選択", list(store_options.keys()), help="レビューを投稿する店舗を選択してください")
        selected_store_id = store_options[selected_store_name]
        
        with st.form("review_form", clear_on_submit=True):
            user_name = st.text_input("👤 ユーザー名（メールアドレスまたは表示名）*", "", help="レビュー投稿者名を入力してください")
            
            # 評価入力（FB-3対応：星で表示）
            st.markdown("⭐ **評価**（1〜5の星）*")
            rating = st.slider("", 1, 5, 3, help="1が最低、5が最高評価です")
            st.markdown(f"選択中の評価: {'⭐' * rating}{'☆' * (5 - rating)} ({rating}/5)")
            
            comment = st.text_area("💬 コメント*", "", help="レビューコメントを入力してください", height=100)
            
            submitted = st.form_submit_button("📝 レビューを投稿する", use_container_width=True)
            
            if submitted:
                if user_name and comment:
                    # 選択された店舗を検索
                    store_index = None
                    for i, store in enumerate(stores):
                        if store.get('id') == selected_store_id:
                            store_index = i
                            break
                    
                    if store_index is not None:
                        # レビューを追加
                        new_review = {
                            "user": user_name,
                            "rating": rating,
                            "comment": comment,
                            "date": datetime.now().strftime("%Y-%m-%d")
                        }
                        
                        stores[store_index]['reviews'].append(new_review)
                        
                        # 評価を再計算
                        stores[store_index]['rating'] = calculate_rating(stores[store_index]['reviews'])
                        
                        # データを保存
                        save_stores(stores, rerun=False)
                        
                        # 成功メッセージ（FB-5対応：一度だけ表示）
                        st.session_state.show_success = True
                        st.session_state.success_message = f"✅ レビューを投稿しました！"
                        st.session_state.show_balloons = True
                        
                        # リロードして反映（FB-2, FB-4対応）
                        st.rerun()
                    else:
                        st.error("⚠️ 店舗が見つかりませんでした。")
                else:
                    st.error("⚠️ 必須項目（*）を入力してください。")

# フッター
st.markdown("---")
st.markdown("<div style='text-align: center; color: #666;'>**Panasonic Lunch Navi** - 社員同士の情報が温かく循環するランチ紹介アプリ</div>", unsafe_allow_html=True)

# 成功メッセージと風船の表示（FB-5対応：一度だけ表示）
if st.session_state.show_success:
    st.success(st.session_state.success_message)
    if st.session_state.show_balloons:
        st.balloons()
        st.session_state.show_balloons = False
    st.session_state.show_success = False
